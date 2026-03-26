@echo off
echo Installing Oil Price Game...
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Initialize database
echo Initializing database...
python -c "from database_handler import DatabaseHandler; h = DatabaseHandler(); h.initialize_database()"

REM Run the app
echo.
echo Starting Oil Price Game...
echo Visit http://localhost:5000 in your browser
echo.
python app.py
