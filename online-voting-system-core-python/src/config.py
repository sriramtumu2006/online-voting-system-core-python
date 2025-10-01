# src/config.py
import os
from supabase import create_client, Client

def get_supabase() -> Client:
    SUPABASE_URL = os.environ.get("https://hzadoiewjwynbjzylkkv.supabase.co")
    SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6YWRvaWV3and5bmJqenlsa2t2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgxNzA0NjksImV4cCI6MjA3Mzc0NjQ2OX0.vyBgtysLPWevSTnEyq5b7mWt5fh196G6AUyC8n36b6I")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set as environment variables")

    return create_client(SUPABASE_URL, SUPABASE_KEY)
