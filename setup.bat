@echo off
REM GitLab Changelog Generator - Setup Script for Windows
REM This script automates the initial setup process

echo.
echo ========================================
echo GitLab Changelog Generator - Setup
echo ========================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo .env file created
    echo.
    echo WARNING: Please edit .env file and add your credentials:
    echo    - GITLAB_ACCESS_TOKEN
    echo    - GITLAB_PROJECT_ID
    echo    - GEMINI_TOKEN
    echo.
) else (
    echo .env file already exists
    echo.
)

REM Create results directory
if not exist "results" (
    mkdir results
    echo Created results\ directory
) else (
    echo results\ directory already exists
)
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo    1. Edit .env file with your credentials
echo    2. Run: .venv\Scripts\activate.bat
echo    3. Run: python main.py
echo.
echo Documentation:
echo    - Quick Start: QUICKSTART.md
echo    - Full Guide: README.md
echo    - Sample Output: SAMPLE_OUTPUT.md
echo.
echo Happy changelog generating!
echo.
pause
