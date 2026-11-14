import axios from 'axios';
import type { AnalysisResult, ReviewsResponse, DemoProduct } from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 120000,
});

export const analyseProduct = async (url: string) => {
  const res = await api.post('/products/analyse', { url });
  return res.data as { product_id: string; analysis_id: string; cached: boolean };
};

export const getAnalysisStatus = async (analysisId: string) => {
  const res = await api.get(`/analysis/${analysisId}/status`);
  return res.data as {
    id: string; product_id: string; status: string;
    error_message?: string; total_retrieved: number; total_analysed: number;
  };
};

export const getAnalysisResults = async (analysisId: string) => {
  const res = await api.get(`/analysis/${analysisId}/results`);
  return res.data as AnalysisResult;
};

export const getProductReviews = async (
  productId: string,
  params: {
    classification?: string;
    risk_level?: string;
    search?: string;
    sort_by?: string;
    page?: number;
    page_size?: number;
  }
) => {
  const res = await api.get(`/reviews/product/${productId}`, { params });
  return res.data as ReviewsResponse;
};

export const getDemoProducts = async () => {
  const res = await api.get('/demo/products');
  return res.data as { demo_products: DemoProduct[]; note: string };
};

export const compareProducts = async (url1: string, url2: string) => {
  const res = await api.post('/comparison/', { url1, url2 });
  return res.data;
};

export const getComparison = async (analysisId1: string, analysisId2: string) => {
  const res = await api.get(`/comparison/${analysisId1}/${analysisId2}`);
  return res.data;
};

export const getModelPerformance = async () => {
  const res = await api.get('/model/performance');
  return res.data;
};

export const downloadReport = (analysisId: string) => {
  window.open(`/api/reports/${analysisId}/pdf`, '_blank');
};

export default api;
