@echo off
echo ===================================================
echo   Starting TRUSTSCOPE AI (Backend Server)
echo ===================================================
cd backend
"C:\Users\karti\AppData\Local\Python\bin\python.exe" -m uvicorn app.main:app --reload --port 8000
pause
