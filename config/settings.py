"""Configuration settings for Lab-Rador."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Environment and paths
PROJECT_ROOT = Path(__file__).parent.parent
PROTOCOLS_DIR = PROJECT_ROOT / "data" / "protocols"
LOGS_DIR = PROJECT_ROOT / "logs"

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")

# API Keys (Gemini is free, Anthropic is paid)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Gemini Configuration (FREE - 60 requests/minute, 1000/day)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "4096"))
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

# Claude Configuration (PAID - fallback option)
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))
CLAUDE_TEMPERATURE = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))

# protocols.io Configuration
PROTOCOLS_IO_BASE_URL = "https://www.protocols.io/api/v3"

# Demo Mode Configuration
DEMO_MODE = os.getenv("LABRADOR_DEMO_MODE", "false").lower() == "true"

# Validation
def validate_config():
    """Validate required configuration."""
    if DEMO_MODE:
        # Demo mode doesn't need API keys
        pass
    elif GEMINI_API_KEY:
        # Using free Gemini API
        pass
    elif ANTHROPIC_API_KEY:
        # Using paid Anthropic API
        pass
    else:
        raise ValueError(
            "No API key configured. Options:\n"
            "1. Set GEMINI_API_KEY for FREE Google Gemini API\n"
            "2. Set ANTHROPIC_API_KEY for paid Anthropic Claude API\n"
            "3. Set LABRADOR_DEMO_MODE=true for demo mode (no API needed)"
        )

    # Create necessary directories
    PROTOCOLS_DIR.mkdir(exist_ok=True, parents=True)
    LOGS_DIR.mkdir(exist_ok=True, parents=True)

# Initialize validation
validate_config()