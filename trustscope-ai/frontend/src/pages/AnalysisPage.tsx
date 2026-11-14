import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CheckCircle, Circle, Loader2, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';
import { getAnalysisStatus, getAnalysisResults } from '../services/api';
import { useAnalysisStore } from '../store/analysisStore';

const STAGES = [
  'Validating product URL',
  'Identifying shopping platform',
  'Retrieving product information',
  'Collecting customer reviews',
  'Preprocessing review data',
  'Detecting duplicate reviews',
  'Running NLP & ML analysis',
  'Calculating risk scores',
  'Generating product trust report',
];

export const AnalysisPage: React.FC = () => {
  const { analysisId } = useParams<{ analysisId: string }>();
  const navigate = useNavigate();
  const { setAnalysisResult } = useAnalysisStore();
  const [status, setStatus] = useState('pending');
  const [error, setError] = useState<string | null>(null);
  const [currentStage, setCurrentStage] = useState(0);
  const [retrieved, setRetrieved] = useState(0);
  const [analysed, setAnalysed] = useState(0);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (!analysisId) return;

    const poll = async () => {
      try {
        const statusData = await getAnalysisStatus(analysisId);
        setStatus(statusData.status);
        setRetrieved(statusData.total_retrieved || 0);
        setAnalysed(statusData.total_analysed || 0);

        if (statusData.status === 'running') {
          if (statusData.total_retrieved > 0 && currentStage < 4) {
            setCurrentStage(4);
          }
        }

        if (statusData.status === 'done') {
          setCurrentStage(STAGES.length - 1);
          if (intervalRef.current) clearInterval(intervalRef.current);
          const result = await getAnalysisResults(analysisId);
          setAnalysisResult(result);
          setTimeout(() => navigate(`/dashboard/${analysisId}`), 1000);
        }

        if (statusData.status === 'failed') {
          if (intervalRef.current) clearInterval(intervalRef.current);
          setError(statusData.error_message || 'Analysis failed. Please try again.');
        }
      } catch (err) {
        console.error('Status poll error:', err);
      }
    };

    const stageTimer = setInterval(() => {
      setCurrentStage(prev => {
        if (prev < STAGES.length - 2) return prev + 1;
        return prev;
      });
    }, 1800);

    intervalRef.current = setInterval(poll, 1500);
    poll();

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      clearInterval(stageTimer);
    };
  }, [analysisId]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="card max-w-md w-full text-center">
          <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Analysis Failed</h2>
          <p className="text-slate-400 mb-6 text-sm">{error}</p>
          <button onClick={() => navigate('/')} className="btn-primary w-full">Return Home</button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-lg w-full">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-blue-600/20 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-blue-500/30">
              <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-1">Analysing Product Reviews</h2>
            <p className="text-slate-400 text-sm">Evaluating linguistic patterns, duplication, and ML signals...</p>
          </div>

          {/* Stages list */}
          <div className="space-y-3 mb-8">
            {STAGES.map((stage, i) => {
              const done = i < currentStage;
              const active = i === currentStage;
              return (
                <div key={i} className={`flex items-center gap-3 transition-all ${active ? 'opacity-100 scale-102' : done ? 'opacity-70' : 'opacity-30'}`}>
                  <div className="flex-shrink-0">
                    {done ? (
                      <CheckCircle className="w-5 h-5 text-emerald-400" />
                    ) : active ? (
                      <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
                    ) : (
                      <Circle className="w-5 h-5 text-slate-700" />
                    )}
                  </div>
                  <span className={`text-sm font-medium ${active ? 'text-blue-300 font-semibold' : done ? 'text-slate-300' : 'text-slate-600'}`}>
                    {stage}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Counts */}
          {(retrieved > 0 || analysed > 0) && (
            <div className="bg-slate-800/60 rounded-xl p-4 text-center border border-slate-700/60 mb-4">
              <div className="flex justify-around">
                <div>
                  <div className="text-2xl font-bold text-blue-400">{retrieved}</div>
                  <div className="text-xs text-slate-400">Reviews Collected</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-violet-400">{analysed}</div>
                  <div className="text-xs text-slate-400">Processed by NLP</div>
                </div>
              </div>
            </div>
          )}

          {/* Progress bar */}
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-blue-500 to-violet-500"
              initial={{ width: '10%' }}
              animate={{ width: `${Math.min(100, ((currentStage + 1) / STAGES.length) * 100)}%` }}
              transition={{ duration: 0.4 }}
            />
          </div>
        </motion.div>
      </div>
    </div>
  );
};
