import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster position="top-right" toastOptions={{
        style: { background: '#1e293b', color: '#fff', borderRadius: '12px', border: '1px solid #334155' },
        success: { style: { background: '#064e3b', color: '#6ee7b7' } },
        error: { style: { background: '#7f1d1d', color: '#fca5a5' } },
      }} />
    </BrowserRouter>
  </React.StrictMode>
)
