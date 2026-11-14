import React, { useState } from 'react';
import { GitCompare, Zap, AlertTriangle, CheckCircle, TrendingDown, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { compareProducts, getComparison, getAnalysisStatus } from '../services/api';

interface ComparisonResult {
  product1: any;
  product2: any;
}

export const ComparisonPage: React.FC = () => {
  const [url1, setUrl1] = useState('');
  const [url2, setUrl2] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComparisonResult | null>(null);

  const handleCompare = async () => {
    if (!url1.trim() || !url2.trim()) { toast.error('Please enter both product URLs'); return; }
    setLoading(true);
    try {
      const { analysis1_id, analysis2_id } = await compareProducts(url1, url2);
      
      const poll = async () => {
        const [s1, s2] = await Promise.all([
          getAnalysisStatus(analysis1_id),
          getAnalysisStatus(analysis2_id),
        ]);
        if (s1.status === 'done' && s2.status === 'done') {
          const compData = await getComparison(analysis1_id, analysis2_id);
          setResult(compData);
          setLoading(false);
        } else if (s1.status === 'failed' || s2.status === 'failed') {
          toast.error('One or both analyses encountered an issue.');
          setLoading(false);
        } else {
          setTimeout(poll, 1500);
        }
      };
      await poll();
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Comparison initiation failed');
      setLoading(false);
    }
  };

  const CompareMetricRow: React.FC<{
    label: string;
    v1: number | string;
    v2: number | string;
    suffix?: string;
    higherIsBetter?: boolean;
  }> = ({ label, v1, v2, suffix = '', higherIsBetter = true }) => {
    const num1 = typeof v1 === 'number' ? v1 : parseFloat(v1 as string) || 0;
    const num2 = typeof v2 === 'number' ? v2 : parseFloat(v2 as string) || 0;
    
    let winner = 0;
    if (num1 !== num2) {
      if (higherIsBetter) {
        winner = num1 > num2 ? 1 : 2;
      } else {
        winner = num1 < num2 ? 1 : 2;
      }
    }

    return (
      <div className="py-3 border-b border-slate-800/80 grid grid-cols-3 items-center text-center">
        <div className={`text-base font-bold ${winner === 1 ? 'text-emerald-400' : 'text-slate-300'}`}>
          {typeof v1 === 'number' ? v1.toFixed(1) : v1}{suffix}
          {winner === 1 && <span className="ml-1 text-xs text-emerald-400">✓</span>}
        </div>
        <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</div>
        <div className={`text-base font-bold ${winner === 2 ? 'text-emerald-400' : 'text-slate-300'}`}>
          {typeof v2 === 'number' ? v2.toFixed(1) : v2}{suffix}
          {winner === 2 && <span className="ml-1 text-xs text-emerald-400">✓</span>}
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-900/30 border border-blue-800 text-xs text-blue-300 font-medium mb-3">
          <GitCompare className="w-3.5 h-3.5" />
          Side-by-Side Review Intelligence
        </div>
        <h1 className="section-title text-3xl font-black">Compare Product Trust Profiles</h1>
        <p className="section-subtitle mb-0">Evaluate two products to determine which one carries more reliable customer reviews.</p>
      </div>

      {/* URL Inputs */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-xs font-medium text-slate-300 mb-1.5 block">Product 1 (Amazon or Flipkart Link)</label>
            <input
              value={url1}
              onChange={e => setUrl1(e.target.value)}
              placeholder="Paste first product link..."
              className="input-primary text-xs"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-300 mb-1.5 block">Product 2 (Amazon or Flipkart Link)</label>
            <input
              value={url2}
              onChange={e => setUrl2(e.target.value)}
              placeholder="Paste second product link..."
              className="input-primary text-xs"
            />
          </div>
        </div>

        {/* 1-Click Demo Shortcut */}
        <div className="mb-4 text-center">
          <span className="text-xs text-slate-500 mr-2">Try Demo Pair:</span>
          <button
            type="button"
            onClick={() => {
              setUrl1('https://www.amazon.com/dp/DEMO001');
              setUrl2('https://www.amazon.com/dp/DEMO002');
            }}
            className="text-xs text-blue-400 hover:text-blue-300 underline font-medium"
          >
            Load Genuine Water Bottle vs. Suspicious Supplement
          </button>
        </div>

        <button
          onClick={handleCompare}
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center gap-2 text-sm"
        >
          {loading ? (
            <>
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Running Parallel AI Analysis on Both Products...
            </>
          ) : (
            <>
              <GitCompare className="w-4 h-4" />
              Compare Both Products
            </>
          )}
        </button>
      </div>

      {/* Results Comparison Grid */}
      {result && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
          {/* Product Header Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="card text-center border-blue-800/60 bg-blue-950/10">
              <span className="badge badge-genuine mb-2">Product A</span>
              <h3 className="font-bold text-white text-sm line-clamp-2 mb-2">{result.product1.product_name || 'Product 1'}</h3>
              <div className="text-4xl font-black text-blue-400">{result.product1.trust_score?.toFixed(1)}</div>
              <div className="text-xs text-slate-400 mt-1">Trust Score (0-100)</div>
            </div>

            <div className="card text-center border-violet-800/60 bg-violet-950/10">
              <span className="badge bg-violet-900/50 text-violet-300 border border-violet-800 mb-2">Product B</span>
              <h3 className="font-bold text-white text-sm line-clamp-2 mb-2">{result.product2.product_name || 'Product 2'}</h3>
              <div className="text-4xl font-black text-violet-400">{result.product2.trust_score?.toFixed(1)}</div>
              <div className="text-xs text-slate-400 mt-1">Trust Score (0-100)</div>
            </div>
          </div>

          {/* Metrics Table */}
          <div className="card">
            <h4 className="font-bold text-white text-sm mb-4">Detailed Metrics Comparison</h4>
            <div className="border-t border-slate-800/80">
              <CompareMetricRow label="Trust Score" v1={result.product1.trust_score} v2={result.product2.trust_score} higherIsBetter={true} />
              <CompareMetricRow label="Genuine-Looking %" v1={result.product1.genuine_pct} v2={result.product2.genuine_pct} suffix="%" higherIsBetter={true} />
              <CompareMetricRow label="Suspicious %" v1={result.product1.suspicious_pct} v2={result.product2.suspicious_pct} suffix="%" higherIsBetter={false} />
              <CompareMetricRow label="Uncertain %" v1={result.product1.uncertain_pct} v2={result.product2.uncertain_pct} suffix="%" higherIsBetter={false} />
              <CompareMetricRow label="Duplicate Reviews" v1={result.product1.duplicate_count} v2={result.product2.duplicate_count} higherIsBetter={false} />
              <CompareMetricRow label="Total Analysed" v1={result.product1.total_analysed} v2={result.product2.total_analysed} />
              <CompareMetricRow label="Reported Rating" v1={result.product1.average_rating} v2={result.product2.average_rating} suffix=" ★" />
              <CompareMetricRow label="Adjusted Rating" v1={result.product1.adjusted_rating} v2={result.product2.adjusted_rating} suffix=" ★" />
            </div>
          </div>

          <div className="card bg-amber-950/20 border-amber-900/60 text-xs text-amber-300">
            <strong>Important Consumer Note:</strong> Review trust analysis measures the authenticity of reviews, not overall product engineering, durability, or seller shipping speed.
          </div>
        </motion.div>
      )}
    </div>
  );
};
