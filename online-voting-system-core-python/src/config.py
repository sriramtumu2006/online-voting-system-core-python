# src/config.py
import os
from supabase import create_client, Client

def get_supabase() -> Client:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set as environment variables")

    return create_client(SUPABASE_URL, SUPABASE_KEY)

