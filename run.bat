@echo off
setlocal enabledelayedexpansion

color 0B

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🤖 Crypto Signal Telegram Bot                               ║
echo ║   Startup Script (Windows)                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
echo 📋 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
color 0A
echo ✅ %PYTHON_VERSION% found
color 0B

REM Check Virtual Environment
echo.
echo 📋 Checking virtual environment...

if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        color 0C
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    color 0A
    echo ✅ Virtual environment created
    color 0B
)

REM Activate Virtual Environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    color 0C
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
color 0A
echo ✅ Virtual environment activated
color 0B

REM Check requirements
echo.
echo 📋 Checking dependencies...

if not exist "requirements.txt" (
    color 0C
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)

REM Install dependencies
pip install -q -r requirements.txt
if errorlevel 1 (
    color 0C
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)

color 0A
echo ✅ Dependencies installed
color 0B

REM Check .env
echo.
echo 📋 Checking configuration...

if not exist ".env" (
    color 0C
    echo ❌ .env file not found
    echo 📝 Please create .env file with:
    echo    TELEGRAM_TOKEN=your_token
    echo    TELEGRAM_CHAT_ID=your_chat_id
    pause
    exit /b 1
)

color 0A
echo ✅ Configuration file found
color 0B

REM Run bot
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║   🚀 Starting Bot...                                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

python main.py
set STATUS=%ERRORLEVEL%

pause
exit /b %STATUS%
