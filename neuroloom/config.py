"""Central config. Loads from .env, falls back to safe defaults."""
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "London")

GEMINI_MODEL = "gemini-2.0-flash"  # swap to "gemini-1.5-flash" if 2.0 isn't enabled
BRIDGE_LENGTH = 5