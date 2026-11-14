import React from 'react';
import { Shield, Cpu, Database, Zap, CheckCircle2, Layers } from 'lucide-react';

export const AboutPage: React.FC = () => (
  <div className="max-w-3xl mx-auto px-4 py-8">
    <div className="text-center mb-10">
      <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-violet-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-xl">
        <Shield className="w-8 h-8 text-white" />
      </div>
      <h1 className="text-4xl font-black text-white mb-2">TRUSTSCOPE AI</h1>
      <p className="text-xl text-blue-400 font-semibold">Know Which Reviews to Trust Before You Buy.</p>
      <p className="text-xs text-slate-500 mt-2">College Hackathon Software Engineering Submission</p>
    </div>

    <div className="space-y-6">
      {/* Problem Statement */}
      <div className="card">
        <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
          <Layers className="w-4 h-4 text-blue-400" />
          The Problem
        </h2>
        <p className="text-slate-300 text-sm leading-relaxed">
          Modern e-commerce platforms host millions of consumer reviews. However, a significant fraction are artificially generated, sponsored, duplicated across products, or incentivized by unscrupulous sellers to artificially inflate product ratings. 
          Consumers cannot easily spot coordinated review spam or subtle promotional patterns, resulting in regrettable purchases and diminished market trust.
        </p>
      </div>

      {/* Proposed Solution */}
      <div className="card">
        <h2 className="text-base font-bold text-white mb-2 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          Our Multi-Tier AI Solution
        </h2>
        <p className="text-slate-300 text-sm leading-relaxed mb-4">
          TrustScope AI eliminates manual review inspection. Users simply paste an Amazon or Flipkart link. The backend autonomously retrieves customer reviews and runs a comprehensive multi-tier analysis pipeline:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {[
            { icon: Zap, label: 'NLP Stylistic Analysis', desc: 'Evaluates promotional phrasing, exclamation count, caps spam, and sentiment-rating divergence via VADER.' },
            { icon: Database, label: 'Duplicate Detection', desc: 'Identifies copy-pasted or template reviews using TF-IDF n-grams & cosine similarity matrices.' },
            { icon: Cpu, label: 'Supervised ML Classifier', desc: 'Trained Logistic Regression, Naive Bayes & Random Forest classifiers predicting deception probability.' },
            { icon: Shield, label: 'Calibrated Risk Scoring', desc: 'Generates an explainable 0–100 risk score and product-level Trust Score with genuine % breakdown.' },
          ].map(({ icon: Icon, label, desc }) => (
            <div key={label} className="bg-slate-800/50 rounded-xl p-3.5 border border-slate-800">
              <Icon className="w-4 h-4 text-blue-400 mb-1.5" />
              <div className="text-sm font-bold text-white">{label}</div>
              <div className="text-xs text-slate-400 leading-relaxed mt-0.5">{desc}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture & Tech Stack */}
      <div className="card">
        <h2 className="text-base font-bold text-white mb-3">Complete Technology Stack</h2>
        <div className="flex flex-wrap gap-2 text-xs">
          {[
            'React 18', 'TypeScript', 'Tailwind CSS', 'Vite', 'Recharts', 'Lucide Icons',
            'FastAPI', 'Python 3.14', 'SQLAlchemy', 'SQLite DB', 'Scikit-Learn',
            'VADER Sentiment', 'ReportLab PDF Generator', 'TF-IDF Vectorizer', 'Joblib'
          ].map(t => (
            <span key={t} className="bg-slate-800/80 text-blue-300 border border-slate-700 px-3 py-1.5 rounded-lg font-medium">
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* Ethical AI Statement */}
      <div className="card bg-amber-950/20 border-amber-900/50">
        <h3 className="text-sm font-bold text-amber-300 mb-1.5">Ethical AI & Fraud Claim Transparency</h3>
        <p className="text-xs text-slate-400 leading-relaxed">
          In strict compliance with consumer protection guidelines, TrustScope AI labels reviews as <em>"Genuine-looking"</em>, <em>"Suspicious"</em>, or <em>"Uncertain"</em>. 
          A suspicious classification represents probabilistic deviation from authentic linguistic and behavioral norms, rather than a definitive legal assertion of fraud.
        </p>
      </div>
    </div>
  </div>
);
