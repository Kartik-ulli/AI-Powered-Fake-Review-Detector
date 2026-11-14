import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Shield, Zap, BarChart2, AlertTriangle, CheckCircle, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { analyseProduct, getDemoProducts } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import type { DemoProduct } from '../types';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { setCurrentAnalysis } = useAnalysisStore();
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [demoProducts, setDemoProducts] = useState<DemoProduct[]>([]);

  useEffect(() => {
    getDemoProducts().then(r => setDemoProducts(r.demo_products)).catch(() => {});
  }, []);

  const handleAnalyse = async (inputUrl?: string) => {
    const targetUrl = inputUrl || url;
    if (!targetUrl.trim()) {
      toast.error('Please enter a product URL');
      return;
    }
    setIsLoading(true);
    try {
      const result = await analyseProduct(targetUrl);
      setCurrentAnalysis(result.analysis_id, result.product_id);
      navigate(`/analysis/${result.analysis_id}`);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || 'Invalid URL. Please use a supported Amazon or Flipkart link, or a demo URL.';
      toast.error(msg);
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    { icon: Shield, label: 'AI Classification', desc: 'ML models classify reviews as genuine, suspicious, or uncertain', color: 'text-blue-400' },
    { icon: BarChart2, label: 'Duplicate Detection', desc: 'TF-IDF cosine similarity detects near-duplicate & copied reviews', color: 'text-violet-400' },
    { icon: Zap, label: 'Risk Scoring', desc: 'Every review gets a 0–100 risk score based on multi-signal NLP metrics', color: 'text-amber-400' },
    { icon: CheckCircle, label: 'Explainable AI', desc: 'Clear reasoning behind each suspicious flag and phrase detection', color: 'text-emerald-400' },
  ];

  return (
    <div className="min-h-screen bg-slate-950 overflow-hidden relative">
      {/* Background radial glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl" />
        <div className="absolute top-40 right-1/4 w-96 h-96 bg-violet-600/10 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-5xl mx-auto px-4 pt-20 pb-16">
        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <div className="inline-flex items-center gap-2 bg-blue-600/10 border border-blue-500/20 text-blue-400 text-xs font-medium px-4 py-2 rounded-full mb-8">
            <Shield className="w-3.5 h-3.5" />
            AI-Powered Review Intelligence & Trust Platform
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black text-white mb-6 leading-tight tracking-tight">
            Know Which Reviews
            <br />
            <span className="bg-gradient-to-r from-blue-400 via-blue-300 to-violet-400 bg-clip-text text-transparent">
              to Trust.
            </span>
          </h1>

          <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed">
            Uncover suspicious product reviews with the power of AI before making your next purchase.
          </p>

          {/* URL Input Form */}
          <div className="max-w-2xl mx-auto">
            <div className="flex flex-col sm:flex-row gap-2 p-2 bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl focus-within:border-blue-500/80 transition-colors">
              <div className="relative flex-1">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input
                  type="url"
                  value={url}
                  onChange={e => setUrl(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleAnalyse()}
                  placeholder="Paste your Amazon or Flipkart product link here..."
                  className="w-full bg-transparent pl-11 pr-4 py-3.5 text-slate-100 placeholder-slate-500 focus:outline-none text-sm"
                />
              </div>
              <button
                onClick={() => handleAnalyse()}
                disabled={isLoading}
                className="btn-primary flex items-center justify-center gap-2 whitespace-nowrap text-sm"
              >
                {isLoading ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Analysing...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    Analyse Product
                  </>
                )}
              </button>
            </div>
            <p className="text-xs text-slate-500 mt-2.5">
              Supports Amazon & Flipkart product URLs · Includes 1-Click Interactive Demo Mode
            </p>
          </div>
        </motion.div>

        {/* Demo Products Section */}
        {demoProducts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mb-16"
          >
            <div className="text-center mb-6">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700 text-xs text-slate-300 font-medium mb-2">
                Hackathon Demo Mode
              </div>
              <h2 className="text-lg font-bold text-slate-200">Try Pre-Loaded Demonstration Products</h2>
              <p className="text-xs text-amber-400/90 flex items-center justify-center gap-1 mt-1">
                <AlertTriangle className="w-3.5 h-3.5" />
                Clearly marked demonstration datasets (simulated for judges)
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {demoProducts.map((demo, i) => (
                <button
                  key={i}
                  onClick={() => handleAnalyse(demo.url)}
                  disabled={isLoading}
                  className="text-left card hover:border-blue-500/50 hover:bg-slate-900/90 transition-all group relative overflow-hidden"
                >
                  <div className="flex items-start justify-between mb-3">
                    <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-blue-900/40 text-blue-300 border border-blue-800/80">
                      {demo.type}
                    </span>
                    <ChevronRight className="w-4 h-4 text-slate-600 group-hover:text-blue-400 group-hover:translate-x-0.5 transition-all" />
                  </div>
                  <h3 className="text-sm font-semibold text-white mb-1.5 line-clamp-2">{demo.name}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{demo.description}</p>
                  <div className="mt-4 flex items-center justify-between text-xs text-slate-500 border-t border-slate-800/80 pt-3">
                    <span className="text-amber-400 font-medium">★ {demo.rating}</span>
                    <span className="text-blue-400 text-xs font-medium">Click to analyse →</span>
                  </div>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Feature Highlights */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
          {features.map(({ icon: Icon, label, desc, color }) => (
            <div key={label} className="card text-center">
              <Icon className={`w-6 h-6 ${color} mx-auto mb-3`} />
              <h3 className="text-sm font-semibold text-white mb-1">{label}</h3>
              <p className="text-xs text-slate-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
};
