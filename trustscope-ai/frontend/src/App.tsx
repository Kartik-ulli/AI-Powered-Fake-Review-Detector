import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Layout } from './components/layout/Layout';
import { LandingPage } from './pages/LandingPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { DashboardPage } from './pages/DashboardPage';
import { ReviewExplorerPage } from './pages/ReviewExplorerPage';
import { ComparisonPage } from './pages/ComparisonPage';
import { ModelPerformancePage } from './pages/ModelPerformancePage';
import { AboutPage } from './pages/AboutPage';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/analysis/:analysisId" element={<AnalysisPage />} />
        <Route path="/dashboard/:analysisId" element={<DashboardPage />} />
        <Route path="/reviews/:productId" element={<ReviewExplorerPage />} />
        <Route path="/compare" element={<ComparisonPage />} />
        <Route path="/model-performance" element={<ModelPerformancePage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Layout>
  );
}
