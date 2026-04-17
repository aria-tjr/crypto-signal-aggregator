#!/bin/bash

# Ensure we run from the script's directory so relative paths work
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# رنگ‌ها برای خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🤖 Crypto Signal Telegram Bot                               ║${NC}"
echo -e "${BLUE}║   Startup Script                                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# بررسی Python
echo -e "${YELLOW}📋 Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# بررسی Virtual Environment
echo ""
echo -e "${YELLOW}📋 Checking virtual environment...${NC}"

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# فعال‌کردن Virtual Environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
# shellcheck disable=SC1091
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# بررسی requirements
echo ""
echo -e "${YELLOW}📋 Checking dependencies...${NC}"

if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

# نصب dependencies (core)
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Error installing dependencies from requirements.txt${NC}"
    deactivate
    exit 1
fi

# نصب اختیاری: extras
if [ -n "${INSTALL_OPTIONAL}" ] && [ -f "requirements-optional.txt" ]; then
    echo -e "${YELLOW}📦 Installing optional packages (INSTALL_OPTIONAL=${INSTALL_OPTIONAL})...${NC}"
    pip install -q -r requirements-optional.txt || echo -e "${YELLOW}⚠️  Optional packages failed to install. Continuing...${NC}"
fi

# نصب dev/test (اختیاری)
if [ -n "${INSTALL_DEV}" ] && [ -f "requirements-dev.txt" ]; then
    echo -e "${YELLOW}🧪 Installing dev/test packages (INSTALL_DEV=${INSTALL_DEV})...${NC}"
    pip install -q -r requirements-dev.txt || echo -e "${YELLOW}⚠️  Dev packages failed to install. Continuing...${NC}"
fi

# بررسی .env
echo ""
echo -e "${YELLOW}📋 Checking configuration...${NC}"

if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    echo -e "${YELLOW}📝 Please create .env file with:${NC}"
    echo "   TELEGRAM_TOKEN=your_token"
    echo "   TELEGRAM_CHAT_ID=your_chat_id"
    deactivate
    exit 1
fi

echo -e "${GREEN}✅ Configuration file found${NC}"

# اجرای برنامه
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🚀 Starting Bot...                                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

python3 main.py
STATUS=$?

# Deactivate venv
deactivate

exit ${STATUS}
