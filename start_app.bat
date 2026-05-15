@echo off
cd /d "%~dp0"
echo Starting Aaj K Garne?...
start "Backend" /B python run_backend.py
timeout /t 3 >nul
start "Frontend" http://localhost:8501
python -m streamlit run frontend\app.py --server.port 8501
