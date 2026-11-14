import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Shield, AlertTriangle, CheckCircle, HelpCircle, Download, Search, Star, TrendingDown, Copy, BarChart2, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { getAnalysisResults, downloadReport } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';
import type { AnalysisResult } from '../types';

const COLORS = { genuine: '#10b981', suspicious: '#ef4444', uncertain: '#f59e0b' };

const TrustScoreRing: React.FC<{ score: number }> = ({ score }) => {
  const color = score >= 70 ? '#10b981' : score >= 40 ? '#f59e0b' : '#ef4444';
  const label = score >= 70 ? 'Trustworthy' : score >= 40 ? 'Moderate Risk' : 'High Suspicion';
  const radius = 48;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="relative w-36 h-36 mx-auto flex items-center justify-center">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle
          cx="60" cy="60" r={radius} fill="none"
          stroke={color} strokeWidth="10"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-3xl font-black text-white">{Math.round(score)}</span>
        <span className="text-[11px] font-semibold tracking-wide uppercase mt-0.5" style={{ color }}>{label}</span>
      </div>
    </div>
  );
};

const StatCard: React.FC<{ label: string; value: string | number; sub?: string; color?: string; icon: React.ReactNode }> = ({ label, value, sub, color = 'text-white', icon }) => (
  <div className="card">
    <div className="flex items-start justify-between mb-2">
      <span className="text-xs text-slate-400 font-medium uppercase tracking-wide">{label}</span>
      <div className="text-slate-500">{icon}</div>
    </div>
    <div className={`text-3xl font-bold ${color} mb-0.5`}>{value}</div>
    {sub && <div className="text-xs text-slate-500">{sub}</div>}
  </div>
);

export const DashboardPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const { analysisResult, setAnalysisResult } = useAnalysisStore();
  const [result, setResult] = useState<AnalysisResult | null>(analysisResult);
  const [loading, setLoading] = useState(!analysisResult);

  useEffect(() => {
    if (analysisId) {
      setLoading(true);
      getAnalysisResults(analysisId)
        .then(r => { setResult(r); setAnalysisResult(r); })
        .catch(() => navigate('/'))
        .finally(() => setLoading(false));
    }
  }, [analysisId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-slate-400">Loading Product Trust Dashboard...</p>
        </div>
      </div>
    );
  }

  if (!result) return null;
  const { product, summary } = result;

  const pieData = [
    { name: 'Genuine', value: Number(summary.genuine_pct.toFixed(1)), count: summary.genuine_count },
    { name: 'Suspicious', value: Number(summary.suspicious_pct.toFixed(1)), count: summary.suspicious_count },
    { name: 'Uncertain', value: Number(summary.uncertain_pct.toFixed(1)), count: summary.uncertain_count },
  ].filter(d => d.count > 0);

  const riskData = [
    { name: 'Low Risk', value: summary.low_risk_count, fill: '#10b981' },
    { name: 'Medium Risk', value: summary.medium_risk_count, fill: '#f59e0b' },
    { name: 'High Risk', value: summary.high_risk_count, fill: '#ef4444' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Product Banner */}
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="card mb-6">
        <div className="flex flex-col md:flex-row items-start gap-6">
          {product.product_image && (
            <img src={product.product_image} alt={product.product_name} 
                 className="w-28 h-28 object-cover rounded-xl border border-slate-700 flex-shrink-0 bg-slate-800" 
                 onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
            />
          )}
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="badge badge-genuine uppercase font-semibold">{product.platform}</span>
              {product.is_demo && (
                <span className="badge bg-amber-900/50 text-amber-300 border border-amber-800 font-semibold">
                  DEMO DATASET
                </span>
              )}
            </div>
            <h1 className="text-2xl font-bold text-white mb-2 line-clamp-2">{product.product_name || 'Product'}</h1>
            <div className="flex flex-wrap items-center gap-5 text-sm text-slate-400">
              <span className="flex items-center gap-1.5 font-medium text-amber-400">
                <Star className="w-4 h-4 fill-amber-400" />
                {product.average_rating ? Number(product.average_rating).toFixed(1) : 'N/A'} original rating
              </span>
              <span>{product.total_reviews_count || summary.total_retrieved} total reviews</span>
              <span className="text-blue-400 font-medium">{summary.total_analysed} reviews analysed</span>
            </div>
          </div>
          <div className="flex flex-wrap gap-2.5 mt-2 md:mt-0">
            <button onClick={() => downloadReport(analysisId!)} className="btn-secondary text-sm flex items-center gap-2">
              <Download className="w-4 h-4 text-blue-400" /> Download PDF Report
            </button>
            <Link to={`/reviews/${result.product.id}`} className="btn-primary text-sm flex items-center gap-2">
              <Search className="w-4 h-4" /> Explore Suspicious Reviews
            </Link>
          </div>
        </div>
        {product.is_demo && (
          <div className="mt-4 p-3 bg-amber-950/40 border border-amber-800/80 rounded-xl text-xs text-amber-300 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 flex-shrink-0 text-amber-400" />
            <span>Note for judges: This analysis is based on <strong>simulated demonstration data</strong>. These are not real product reviews.</span>
          </div>
        )}
      </motion.div>

      {/* Trust Score + The 3 Core Percentage Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }} className="card flex flex-col items-center justify-center text-center">
          <div className="text-xs text-slate-400 uppercase font-semibold tracking-wider mb-2">Overall Trust Score</div>
          <TrustScoreRing score={summary.trust_score} />
          <div className="text-xs text-slate-500 mt-2">Scale: 0 (Unreliable) to 100 (Authentic)</div>
        </motion.div>

        {/* Genuine Card */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className="card flex flex-col items-center justify-center text-center border-emerald-800/60 bg-emerald-950/10">
          <CheckCircle className="w-7 h-7 text-emerald-400 mb-2" />
          <div className="text-5xl font-black text-emerald-400 tracking-tight">{summary.genuine_pct.toFixed(1)}%</div>
          <div className="text-sm font-semibold text-slate-200 mt-2">Genuine-looking Reviews</div>
          <div className="text-xs text-slate-400 mt-0.5">{summary.genuine_count} of {summary.total_analysed} reviews</div>
        </motion.div>

        {/* Suspicious Card */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="card flex flex-col items-center justify-center text-center border-red-800/60 bg-red-950/10">
          <AlertTriangle className="w-7 h-7 text-red-400 mb-2" />
          <div className="text-5xl font-black text-red-400 tracking-tight">{summary.suspicious_pct.toFixed(1)}%</div>
          <div className="text-sm font-semibold text-slate-200 mt-2">Suspicious Reviews</div>
          <div className="text-xs text-slate-400 mt-0.5">{summary.suspicious_count} of {summary.total_analysed} reviews</div>
        </motion.div>

        {/* Uncertain Card */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }} className="card flex flex-col items-center justify-center text-center border-amber-800/60 bg-amber-950/10">
          <HelpCircle className="w-7 h-7 text-amber-400 mb-2" />
          <div className="text-5xl font-black text-amber-400 tracking-tight">{summary.uncertain_pct.toFixed(1)}%</div>
          <div className="text-sm font-semibold text-slate-200 mt-2">Uncertain Reviews</div>
          <div className="text-xs text-slate-400 mt-0.5">{summary.uncertain_count} of {summary.total_analysed} reviews</div>
        </motion.div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Suspicious" value={summary.suspicious_count} icon={<AlertTriangle className="w-4 h-4" />} color="text-red-400" sub="Flagged by AI engine" />
        <StatCard label="Duplicate Reviews" value={summary.duplicate_count} icon={<Copy className="w-4 h-4" />} color="text-violet-400" sub="TF-IDF near-identical" />
        <StatCard label="Original Rating" value={product.average_rating ? `${Number(product.average_rating).toFixed(1)} ★` : 'N/A'} icon={<Star className="w-4 h-4" />} color="text-amber-400" sub="Reported on platform" />
        <StatCard label="Risk-Adjusted Rating" value={summary.adjusted_rating ? `${Number(summary.adjusted_rating).toFixed(1)} ★` : 'N/A'} icon={<TrendingDown className="w-4 h-4" />} color="text-blue-400" sub="Genuine-weighted estimate" />
      </div>

      {/* Visualizations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Classification Donut Chart */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} className="card">
          <h3 className="section-title text-base font-bold text-white mb-2">Review Classification Distribution</h3>
          <p className="text-xs text-slate-400 mb-4">Calculated from verified review analysis</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={4} dataKey="value">
                  {pieData.map((entry, i) => (
                    <Cell key={i} fill={COLORS[entry.name.toLowerCase() as keyof typeof COLORS]} />
                  ))}
                </Pie>
                <Tooltip formatter={(v: any) => [`${Number(v).toFixed(1)}%`, 'Percentage']} contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                <Legend formatter={v => <span className="text-slate-300 text-xs font-medium">{v}</span>} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Risk Level Bar Chart */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.35 }} className="card">
          <h3 className="section-title text-base font-bold text-white mb-2">Review Risk Breakdown</h3>
          <p className="text-xs text-slate-400 mb-4">Low Risk (0-30), Medium Risk (31-60), High Risk (61-100)</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {riskData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Legal & Technical Transparency Disclaimer */}
      <div className="card border-blue-900/40 bg-blue-950/20">
        <div className="flex items-start gap-3">
          <Shield className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="text-sm font-semibold text-blue-300 mb-1">Ethical AI & Compliance Transparency</h4>
            <p className="text-xs text-slate-400 leading-relaxed">
              A suspicious review is <strong>not definitively a fake review</strong>. TrustScope AI calculates risk probabilities based on linguistic indicators, promotional patterns, duplicate detection, and machine learning models. 
              Review trust evaluation does not establish overall product quality or merchant integrity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
