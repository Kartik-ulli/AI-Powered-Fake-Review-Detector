@echo off
echo ===============================================================
echo     TRUSTSCOPE AI - Know Which Reviews to Trust Before You Buy
echo ===============================================================
echo.
echo 1. Starting Backend Server on http://localhost:8000
start "TrustScope Backend" cmd /k "start_backend.bat"
echo.
echo 2. Starting Frontend Dev Server on http://localhost:5173
start "TrustScope Frontend" cmd /k "start_frontend.bat"
echo.
echo Open http://localhost:5173 in your browser to start.
echo (Or visit http://localhost:8000 for the unified production build)
echo.
pause
