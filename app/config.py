import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")
