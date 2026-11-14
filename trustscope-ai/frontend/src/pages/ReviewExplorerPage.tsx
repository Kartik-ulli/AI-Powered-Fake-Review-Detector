import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Search, ChevronLeft, ChevronRight, Star, AlertTriangle, CheckCircle, HelpCircle, Copy, ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';
import { getProductReviews } from '../services/api';
import type { Review } from '../types';

const RiskBadge: React.FC<{ score: number }> = ({ score }) => {
  if (score >= 61) return <span className="badge badge-suspicious font-bold">High Risk · {score}</span>;
  if (score >= 31) return <span className="badge badge-uncertain font-bold">Medium Risk · {score}</span>;
  return <span className="badge badge-genuine font-bold">Low Risk · {score}</span>;
};

const ClassificationBadge: React.FC<{ cls: string }> = ({ cls }) => {
  if (cls === 'genuine') return <span className="badge badge-genuine"><CheckCircle className="w-3 h-3" /> Genuine-looking</span>;
  if (cls === 'suspicious') return <span className="badge badge-suspicious"><AlertTriangle className="w-3 h-3" /> Suspicious</span>;
  return <span className="badge badge-uncertain"><HelpCircle className="w-3 h-3" /> Uncertain</span>;
};

const ReviewCard: React.FC<{ review: Review }> = ({ review }) => {
  const [expanded, setExpanded] = useState(false);
  const textShort = review.text.length > 250 ? review.text.slice(0, 250) + '...' : review.text;

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="card mb-4 hover:border-slate-700/80 transition-colors">
      <div className="flex flex-wrap items-start justify-between gap-3 mb-3">
        <div className="flex flex-wrap items-center gap-2">
          <ClassificationBadge cls={review.classification} />
          <RiskBadge score={review.risk_score} />
          {review.duplicate_group_id && (
            <span className="badge bg-violet-900/50 text-violet-300 border border-violet-800">
              <Copy className="w-3 h-3" /> Duplicate Group
            </span>
          )}
          {review.verified_purchase && (
            <span className="badge bg-slate-800 text-slate-300 border border-slate-700">✓ Verified Purchase</span>
          )}
        </div>
        <div className="flex items-center gap-1 text-amber-400 text-sm font-semibold">
          {'★'.repeat(Math.min(5, Math.max(0, Math.floor(review.rating || 0))))}
          {'☆'.repeat(Math.max(0, 5 - Math.min(5, Math.max(0, Math.floor(review.rating || 0)))))}
          <span className="text-slate-400 ml-1 text-xs">({review.rating}★)</span>
        </div>
      </div>

      {review.title && <h4 className="font-bold text-white text-sm mb-2">"{review.title}"</h4>}
      
      <p className="text-slate-300 text-sm leading-relaxed mb-3">
        {expanded ? review.text : textShort}
        {review.text.length > 250 && (
          <button onClick={() => setExpanded(!expanded)} className="text-blue-400 hover:text-blue-300 ml-2 text-xs font-medium">
            {expanded ? 'Show less' : 'Read full review'}
          </button>
        )}
      </p>

      <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mb-3 border-t border-slate-800/60 pt-2.5">
        <span>Reviewer: <strong className="text-slate-400">{review.reviewer_name || 'Anonymous'}</strong></span>
        {review.date && <span>Date: {review.date}</span>}
        {review.helpful_votes > 0 && <span>{review.helpful_votes} helpful votes</span>}
        {review.ml_confidence > 0 && (
          <span className="text-blue-400/80">ML Model: {review.ml_prediction} ({(review.ml_confidence * 100).toFixed(0)}% conf)</span>
        )}
      </div>

      {review.detection_reasons && review.detection_reasons.length > 0 && (
        <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800">
          <div className="text-xs font-semibold text-amber-400 mb-1.5 flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5" />
            Detected Reasons & Explainable AI Signals:
          </div>
          <ul className="space-y-1">
            {review.detection_reasons.map((reason, i) => (
              <li key={i} className="text-xs text-slate-300 flex items-start gap-1.5">
                <span className="text-amber-500 font-bold">•</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
};

const FILTERS = [
  { value: '', label: 'All Classifications' },
  { value: 'genuine', label: 'Genuine-looking' },
  { value: 'suspicious', label: 'Suspicious' },
  { value: 'uncertain', label: 'Uncertain' },
];

const RISK_FILTERS = [
  { value: '', label: 'All Risk Levels' },
  { value: 'high', label: 'High Risk (61-100)' },
  { value: 'medium', label: 'Medium Risk (31-60)' },
  { value: 'low', label: 'Low Risk (0-30)' },
];

const SORT_OPTIONS = [
  { value: 'risk_score_desc', label: 'Highest Risk Score' },
  { value: 'risk_score_asc', label: 'Lowest Risk Score' },
  { value: 'rating_desc', label: 'Highest Star Rating' },
  { value: 'rating_asc', label: 'Lowest Star Rating' },
];

export const ReviewExplorerPage: React.FC = () => {
  const { productId } = useParams<{ productId: string }>();
  const [reviews, setReviews] = useState<Review[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [classification, setClassification] = useState('');
  const [riskLevel, setRiskLevel] = useState('');
  const [sortBy, setSortBy] = useState('risk_score_desc');
  const [search, setSearch] = useState('');
  const [searchInput, setSearchInput] = useState('');

  const fetchReviews = useCallback(async () => {
    if (!productId) return;
    setLoading(true);
    try {
      const data = await getProductReviews(productId, {
        classification: classification || undefined,
        risk_level: riskLevel || undefined,
        sort_by: sortBy,
        search: search || undefined,
        page,
        page_size: 15,
      });
      setReviews(data.reviews);
      setTotal(data.total);
      setTotalPages(data.total_pages);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [productId, classification, riskLevel, sortBy, search, page]);

  useEffect(() => { fetchReviews(); }, [fetchReviews]);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="section-title">Explore Suspicious Reviews</h1>
          <p className="section-subtitle mb-0">Total reviews: {total} · Filtered by AI risk classification & signals</p>
        </div>
        <button onClick={() => window.history.back()} className="btn-secondary text-xs flex items-center gap-1.5 self-start">
          <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input
              value={searchInput}
              onChange={e => setSearchInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') { setSearch(searchInput); setPage(1); } }}
              placeholder="Search in reviews..."
              className="input-primary pl-9 py-2 text-xs"
            />
          </div>
          <select value={classification} onChange={e => { setClassification(e.target.value); setPage(1); }} className="input-primary py-2 text-xs">
            {FILTERS.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
          </select>
          <select value={riskLevel} onChange={e => { setRiskLevel(e.target.value); setPage(1); }} className="input-primary py-2 text-xs">
            {RISK_FILTERS.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
          </select>
          <select value={sortBy} onChange={e => { setSortBy(e.target.value); setPage(1); }} className="input-primary py-2 text-xs">
            {SORT_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
          </select>
        </div>
      </div>

      {/* Review List */}
      {loading ? (
        <div className="text-center py-16 text-slate-400">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          Loading reviews...
        </div>
      ) : reviews.length === 0 ? (
        <div className="card text-center py-12 text-slate-400">
          No reviews found matching the selected filters.
        </div>
      ) : (
        <>
          {reviews.map(r => <ReviewCard key={r.id} review={r} />)}
          
          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-6">
              <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary text-xs flex items-center gap-1">
                <ChevronLeft className="w-4 h-4" /> Previous
              </button>
              <span className="text-xs text-slate-400 font-medium">Page {page} of {totalPages}</span>
              <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page === totalPages} className="btn-secondary text-xs flex items-center gap-1">
                Next <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};
