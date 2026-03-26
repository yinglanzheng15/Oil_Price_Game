@echo off
echo Verifying Oil Price Game setup...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    exit /b 1
)

echo ✓ Python found

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

echo ✓ Dependencies installed

REM Initialize database
echo Initializing database...
python -c "from database_handler import DatabaseHandler; h = DatabaseHandler(); h.initialize_database(); print('✓ Database initialized')"

REM Test imports
echo Testing imports...
python -c "from app import app, handler; from scoring import calculate_points; print('✓ All imports working')"

echo.
echo ✅ Setup complete! Ready to run:
echo.
echo   Local mode: python app.py
echo   Or: python start.bat
echo.
echo For cloud deployment, see DEPLOY.md
