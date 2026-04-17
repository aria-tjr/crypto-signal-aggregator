"""
Helper script برای راه‌اندازی سیستم
"""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path


def main() -> int:
    """راه‌اندازی برنامه"""

    print("\n" + "=" * 70)
    print("🚀 Crypto Signal Bot - Startup Helper")
    print("=" * 70 + "\n")

    project_root = Path(__file__).parent
    os.chdir(project_root)

    # بررسی .env
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("\nPlease create .env file in the project root with:")
        print("   TELEGRAM_TOKEN=your_telegram_bot_token")
        print("   TELEGRAM_CHAT_ID=your_chat_id")
        print("\nOther optional settings:")
        print("   REDDIT_CLIENT_ID=your_reddit_client_id")
        print("   REDDIT_CLIENT_SECRET=your_reddit_client_secret")
        print("   OPENAI_API_KEY=your_openai_api_key")
        return 1

    # بررسی virtual environment
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=False)
        print("✅ Virtual environment created\n")

    # اجرای برنامه
    print("🚀 Starting bot...\n")

    if sys.platform == "win32":
        # Windows
        python_exec = str(project_root / "venv" / "Scripts" / "python.exe")
    else:
        # Linux/macOS
        python_exec = str(project_root / "venv" / "bin" / "python")

    if not Path(python_exec).exists():
        # fallback to system python
        python_exec = sys.executable

    result = subprocess.run([python_exec, "main.py"])  # nosec - local execution
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
