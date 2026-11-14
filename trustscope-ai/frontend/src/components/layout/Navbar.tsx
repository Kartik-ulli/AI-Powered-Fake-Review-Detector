import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Shield, GitCompare, Info, Cpu } from 'lucide-react';
import { clsx } from 'clsx';

const navItems = [
  { path: '/', label: 'Home', icon: Shield },
  { path: '/model-performance', label: 'AI Model', icon: Cpu },
  { path: '/compare', label: 'Compare', icon: GitCompare },
  { path: '/about', label: 'About', icon: Info },
];

export const Navbar: React.FC = () => {
  const location = useLocation();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/90 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-violet-600 rounded-lg flex items-center justify-center shadow-lg group-hover:shadow-blue-500/30 transition-shadow">
              <Shield className="w-4 h-4 text-white" />
            </div>
            <span className="font-bold text-white text-lg">
              Trust<span className="text-blue-400">Scope</span>
              <span className="text-xs text-violet-400 font-normal ml-1">AI</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-1">
            {navItems.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                className={clsx(
                  'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                  location.pathname === path
                    ? 'bg-blue-600/20 text-blue-400'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                )}
              >
                <Icon className="w-3.5 h-3.5" />
                {label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <span className="hidden sm:flex items-center gap-1 text-xs text-emerald-400 bg-emerald-900/30 border border-emerald-800 px-2.5 py-1 rounded-full">
              <span className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
              AI Engine Ready
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
};
