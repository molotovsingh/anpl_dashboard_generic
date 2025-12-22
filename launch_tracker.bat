@echo off
REM AdNexus Tracker Launcher for Windows
REM Makes it easy to run the investment tracker

echo ================================================
echo    AdNexus - Vinmo Investment Tracker v1.0     
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    echo        Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Streamlit is installed
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install streamlit pandas numpy plotly
    echo Packages installed
    echo.
)

REM Launch the app
echo ================================================
echo Launching AdNexus Tracker...
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Run Streamlit
streamlit run adnexus_tracker_app.py --server.port 8501 --server.address localhost

REM Deactivate virtual environment when done
deactivate

pause