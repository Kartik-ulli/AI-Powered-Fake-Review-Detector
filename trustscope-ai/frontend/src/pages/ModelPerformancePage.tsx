import React, { useEffect, useState } from 'react';
import { Cpu, CheckCircle, BarChart3, Database } from 'lucide-react';
import { getModelPerformance } from '../services/api';

export const ModelPerformancePage: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModelPerformance().then(setData).catch(console.error).finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="mb-8 text-center sm:text-left">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-900/30 border border-blue-800 text-xs text-blue-300 font-medium mb-3">
          <Cpu className="w-3.5 h-3.5" />
          Machine Learning Pipeline Evaluation
        </div>
        <h1 className="section-title text-3xl font-black">AI Model Performance & Benchmarks</h1>
        <p className="section-subtitle mb-0">Empirical evaluation metrics trained and validated on labelled fake-review datasets.</p>
      </div>

      {loading ? (
        <div className="text-center text-slate-400 py-16">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          Loading machine learning metrics...
        </div>
      ) : data ? (
        <div className="space-y-6">
          {/* Best Model Banner */}
          <div className="card border-blue-800/60 bg-blue-950/20">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-600/30 rounded-xl flex items-center justify-center border border-blue-500/40">
                  <Cpu className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <h3 className="font-bold text-white text-lg">Selected Model: {data.best_model_name || 'Logistic Regression (TF-IDF)'}</h3>
                  <p className="text-xs text-slate-400">Chosen automatically via highest cross-validated F1-score</p>
                </div>
              </div>
              <span className="badge badge-genuine px-3 py-1 text-xs font-bold self-start sm:self-auto">
                <CheckCircle className="w-3.5 h-3.5" /> Production Deployed
              </span>
            </div>

            {/* Comparison Overview */}
            {data.all_metrics && (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                {Object.entries(data.all_metrics as Record<string, any>).map(([name, m]: [string, any]) => (
                  <div key={name} className="bg-slate-900/80 rounded-xl p-3 border border-slate-800">
                    <div className="text-xs text-slate-400 font-medium mb-1 truncate">{name}</div>
                    <div className="text-2xl font-black text-blue-400">{(m.f1_score * 100).toFixed(1)}%</div>
                    <div className="text-[11px] text-slate-500">F1-Score · {(m.accuracy * 100).toFixed(1)}% Accuracy</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Model Breakdown Cards */}
          {data.all_metrics && Object.entries(data.all_metrics as Record<string, any>).map(([name, m]: [string, any]) => (
            <div key={name} className="card">
              <div className="flex items-center justify-between mb-4">
                <h4 className="font-bold text-white text-base flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-blue-400" />
                  {name}
                </h4>
                {name === data.best_model_name && <span className="badge badge-genuine">Top Performer</span>}
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
                {[
                  { label: 'Accuracy', val: m.accuracy },
                  { label: 'Precision', val: m.precision },
                  { label: 'Recall', val: m.recall },
                  { label: 'F1-Score', val: m.f1_score },
                ].map(metric => (
                  <div key={metric.label} className="bg-slate-800/40 rounded-xl p-3 text-center border border-slate-800">
                    <div className="text-xl font-black text-white">{(metric.val * 100).toFixed(1)}%</div>
                    <div className="text-xs text-slate-400 font-medium mt-0.5">{metric.label}</div>
                  </div>
                ))}
              </div>

              {/* Confusion Matrix */}
              {m.confusion_matrix && (
                <div>
                  <div className="text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wider">Confusion Matrix (Validation Test Set)</div>
                  <div className="grid grid-cols-2 gap-2 max-w-sm">
                    <div className="bg-emerald-950/40 border border-emerald-800/60 rounded-xl p-2.5 text-center">
                      <div className="text-lg font-black text-emerald-400">{m.confusion_matrix[0][0]}</div>
                      <div className="text-[11px] text-slate-400">True Negative (Genuine)</div>
                    </div>
                    <div className="bg-red-950/40 border border-red-800/60 rounded-xl p-2.5 text-center">
                      <div className="text-lg font-black text-red-400">{m.confusion_matrix[0][1]}</div>
                      <div className="text-[11px] text-slate-400">False Positive (False Flag)</div>
                    </div>
                    <div className="bg-amber-950/40 border border-amber-800/60 rounded-xl p-2.5 text-center">
                      <div className="text-lg font-black text-amber-400">{m.confusion_matrix[1][0]}</div>
                      <div className="text-[11px] text-slate-400">False Negative (Missed)</div>
                    </div>
                    <div className="bg-blue-950/40 border border-blue-800/60 rounded-xl p-2.5 text-center">
                      <div className="text-lg font-black text-blue-400">{m.confusion_matrix[1][1]}</div>
                      <div className="text-[11px] text-slate-400">True Positive (Suspicious)</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Training Context Note */}
          <div className="card bg-slate-900/60 border-slate-800 text-xs text-slate-400 space-y-2">
            <div className="flex items-center gap-1.5 font-semibold text-slate-300">
              <Database className="w-3.5 h-3.5 text-blue-400" />
              Scientific Training Transparency
            </div>
            <p>
              The models were trained on labelled balanced sets with 80/20 train/test split. TF-IDF features capture unigrams and bigrams with sublinear term-frequency scaling. 
              Actual review scoring combines ML probabilities with stylistic NLP markers and TF-IDF duplicate clusters to avoid overfitting.
            </p>
          </div>
        </div>
      ) : (
        <div className="card text-center text-slate-400 py-12">
          Model performance data unavailable.
        </div>
      )}
    </div>
  );
};
