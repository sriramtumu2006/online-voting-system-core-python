# src/config.py
from supabase import create_client, Client

SUPABASE_URL = "https://hzadoiewjwynbjzylkkv.supabase.co"  # replace with your URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6..."  # replace with your key

def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
