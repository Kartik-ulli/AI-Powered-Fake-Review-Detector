export interface Product {
  id: string;
  platform: string;
  product_name: string;
  product_image: string;
  average_rating: number;
  total_reviews_count: string;
  product_url: string;
  is_demo: boolean;
}

export interface AnalysisSummary {
  total_retrieved: number;
  total_analysed: number;
  genuine_count: number;
  suspicious_count: number;
  uncertain_count: number;
  genuine_pct: number;
  suspicious_pct: number;
  uncertain_pct: number;
  trust_score: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  duplicate_count: number;
  adjusted_rating: number | null;
  rating_distribution: Record<string, number>;
  ml_model_info: Record<string, any>;
}

export interface AnalysisResult {
  analysis_id: string;
  product: Product;
  summary: AnalysisSummary;
  timestamp: string;
}

export interface Review {
  id: string;
  text: string;
  title: string;
  rating: number;
  reviewer_name: string;
  date: string;
  verified_purchase: boolean;
  helpful_votes: number;
  risk_score: number;
  classification: 'genuine' | 'suspicious' | 'uncertain';
  detection_reasons: string[];
  suspicious_phrases: string[];
  sentiment_score: number;
  sentiment_label: string;
  similarity_score: number;
  duplicate_group_id: string | null;
  ml_prediction: string;
  ml_confidence: number;
}

export interface ReviewsResponse {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  reviews: Review[];
}

export interface DemoProduct {
  url: string;
  name: string;
  type: string;
  description: string;
  platform: string;
  rating: number;
}

export type RiskLevel = 'high' | 'medium' | 'low';
export type Classification = 'genuine' | 'suspicious' | 'uncertain' | 'all';
