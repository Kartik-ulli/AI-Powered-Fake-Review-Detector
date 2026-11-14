import React from 'react';
import { Navbar } from './Navbar';

interface LayoutProps { children: React.ReactNode; }

export const Layout: React.FC<LayoutProps> = ({ children }) => (
  <div className="min-h-screen bg-slate-950 flex flex-col justify-between">
    <Navbar />
    <main className="pt-16 flex-grow">{children}</main>
    <footer className="border-t border-slate-800/80 py-8 bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 text-center text-slate-500 text-sm">
        <p className="font-medium text-slate-400">TrustScope AI — College Hackathon Edition</p>
        <p className="text-xs text-slate-600 mt-1">
          Built with FastAPI, React, Scikit-Learn & Natural Language Processing.
        </p>
        <p className="text-xs text-slate-600 mt-0.5">
          Results are AI estimates. A suspicious review is not definitively a fake review.
        </p>
      </div>
    </footer>
  </div>
);
