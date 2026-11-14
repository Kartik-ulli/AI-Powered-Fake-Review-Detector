import re
import logging
from typing import List, Dict, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class DuplicateDetector:
    SIMILARITY_THRESHOLD = 0.75  # Reviews above this are "near-duplicates"
    EXACT_THRESHOLD = 0.98
    
    @staticmethod
    def detect(texts: List[str]) -> Dict[int, Dict]:
        """
        Returns a dict mapping review index -> {group_id, max_similarity, is_duplicate}
        """
        if len(texts) < 2:
            return {}
        
        # Preprocess
        clean = [DuplicateDetector._preprocess(t) for t in texts]
        
        try:
            # TF-IDF Vectorization
            vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                min_df=1,
                strip_accents='unicode',
                lowercase=True,
            )
            tfidf_matrix = vectorizer.fit_transform(clean)
            sim_matrix = cosine_similarity(tfidf_matrix)
        except Exception as e:
            logger.warning(f"TF-IDF failed: {e}. Falling back to basic comparison.")
            return DuplicateDetector._basic_detect(texts)
        
        result = {}
        group_id_map = {}  # index -> group_id
        group_counter = [0]
        
        def get_or_create_group(i):
            if i not in group_id_map:
                group_id_map[i] = f"dup_group_{group_counter[0]}"
                group_counter[0] += 1
            return group_id_map[i]
        
        n = len(texts)
        for i in range(n):
            max_sim = 0.0
            for j in range(n):
                if i == j:
                    continue
                sim = float(sim_matrix[i, j])
                if sim > max_sim:
                    max_sim = sim
                if sim >= DuplicateDetector.SIMILARITY_THRESHOLD:
                    # They share a group
                    gi = group_id_map.get(i)
                    gj = group_id_map.get(j)
                    if gi and gj and gi != gj:
                        # Merge groups
                        for k, g in group_id_map.items():
                            if g == gj:
                                group_id_map[k] = gi
                    elif gi:
                        group_id_map[j] = gi
                    elif gj:
                        group_id_map[i] = gj
                    else:
                        new_g = get_or_create_group(i)
                        group_id_map[j] = new_g
            
            result[i] = {
                "max_similarity": min(max_sim, 1.0),
                "group_id": group_id_map.get(i),
                "is_duplicate": max_sim >= DuplicateDetector.SIMILARITY_THRESHOLD,
            }
        
        return result
    
    @staticmethod
    def _preprocess(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text if text else "empty"
    
    @staticmethod
    def _basic_detect(texts: List[str]) -> Dict[int, Dict]:
        result = {}
        for i, t1 in enumerate(texts):
            max_sim = 0.0
            group_id = None
            for j, t2 in enumerate(texts):
                if i == j:
                    continue
                sim = DuplicateDetector._simple_similarity(t1, t2)
                if sim > max_sim:
                    max_sim = sim
                if sim >= 0.75 and not group_id:
                    group_id = f"dup_group_{min(i,j)}"
            result[i] = {"max_similarity": max_sim, "group_id": group_id, "is_duplicate": max_sim >= 0.75}
        return result
    
    @staticmethod
    def _simple_similarity(t1: str, t2: str) -> float:
        s1 = set(t1.lower().split())
        s2 = set(t2.lower().split())
        if not s1 or not s2:
            return 0.0
        return len(s1 & s2) / len(s1 | s2)
