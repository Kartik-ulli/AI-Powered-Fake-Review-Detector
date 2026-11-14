import re
from typing import Optional, Dict
from urllib.parse import urlparse, parse_qs

DEMO_URLS = {
    "demo://genuine-product": {"platform": "demo", "product_id": "DEMO001", "is_demo": True, "demo_type": "genuine"},
    "demo://suspicious-product": {"platform": "demo", "product_id": "DEMO002", "is_demo": True, "demo_type": "suspicious"},
    "demo://mixed-product": {"platform": "demo", "product_id": "DEMO003", "is_demo": True, "demo_type": "mixed"},
    "https://www.amazon.com/dp/DEMO001": {"platform": "demo", "product_id": "DEMO001", "is_demo": True, "demo_type": "genuine"},
    "https://www.amazon.com/dp/DEMO002": {"platform": "demo", "product_id": "DEMO002", "is_demo": True, "demo_type": "suspicious"},
    "https://www.amazon.com/dp/DEMO003": {"platform": "demo", "product_id": "DEMO003", "is_demo": True, "demo_type": "mixed"},
}

class URLParser:
    @staticmethod
    def parse(url: str) -> Optional[Dict]:
        url = url.strip()
        
        # Check demo URLs first
        if url in DEMO_URLS:
            res = dict(DEMO_URLS[url])
            res["url"] = url
            return res
        
        # Check demo:// scheme
        if url.startswith("demo://"):
            demo_type = url.replace("demo://", "").replace("-product", "")
            return {"platform": "demo", "product_id": f"DEMO_{demo_type.upper()}", "is_demo": True, "demo_type": demo_type, "url": url}
        
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc.lower()
            path = parsed.path
            
            # Amazon
            if any(h in hostname for h in ["amazon.com", "amazon.in", "amazon.co.uk", "amazon.de", "amazon.co.jp"]):
                asin = URLParser._extract_amazon_asin(path, parse_qs(parsed.query))
                if asin:
                    return {"platform": "amazon", "product_id": asin, "is_demo": False, "url": url}
            
            # Flipkart
            if "flipkart.com" in hostname:
                pid = URLParser._extract_flipkart_id(path, parse_qs(parsed.query))
                if pid:
                    return {"platform": "flipkart", "product_id": pid, "is_demo": False, "url": url}

            # Generic e-commerce URL support for hackathon testing
            if parsed.scheme in ["http", "https"] and len(path) > 3:
                slug = [s for s in path.split("/") if s][-1]
                return {"platform": hostname.split(".")[0] or "ecommerce", "product_id": slug[:16], "is_demo": False, "url": url}
            
        except Exception:
            pass
        
        return None
    
    @staticmethod
    def _extract_amazon_asin(path: str, query: dict) -> Optional[str]:
        patterns = [
            r'/dp/([A-Z0-9]{10})',
            r'/gp/product/([A-Z0-9]{10})',
            r'/product/([A-Z0-9]{10})',
            r'/([A-Z0-9]{10})(?:/|$)',
        ]
        for pattern in patterns:
            m = re.search(pattern, path)
            if m:
                return m.group(1)
        return None
    
    @staticmethod  
    def _extract_flipkart_id(path: str, query: dict) -> Optional[str]:
        if 'pid' in query:
            return query['pid'][0]
        m = re.search(r'/p/([a-zA-Z0-9]+)', path)
        if m:
            return m.group(1)
        return None
