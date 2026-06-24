import os
from pathlib import Path

# Load .env file before any other imports
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./xczs.db")
