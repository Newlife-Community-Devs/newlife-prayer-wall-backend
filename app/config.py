import os
from dotenv import load_dotenv

load_dotenv()

# Use POSTGRES_URL from Vercel/Supabase, fallback to DATABASE_URL for local dev
DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/prayerdb")

# Fix Supabase/Vercel connection strings: postgres:// -> postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
