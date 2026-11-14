import { create } from 'zustand';
import type { AnalysisResult } from '../types';

interface AnalysisStore {
  currentAnalysisId: string | null;
  currentProductId: string | null;
  analysisResult: AnalysisResult | null;
  analysisStatus: string;
  isLoading: boolean;
  error: string | null;

  setCurrentAnalysis: (analysisId: string, productId: string) => void;
  setAnalysisResult: (result: AnalysisResult) => void;
  setAnalysisStatus: (status: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set) => ({
  currentAnalysisId: null,
  currentProductId: null,
  analysisResult: null,
  analysisStatus: 'idle',
  isLoading: false,
  error: null,

  setCurrentAnalysis: (analysisId, productId) =>
    set({ currentAnalysisId: analysisId, currentProductId: productId }),
  setAnalysisResult: (result) => set({ analysisResult: result }),
  setAnalysisStatus: (status) => set({ analysisStatus: status }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  reset: () => set({
    currentAnalysisId: null, currentProductId: null,
    analysisResult: null, analysisStatus: 'idle',
    isLoading: false, error: null,
  }),
}));
