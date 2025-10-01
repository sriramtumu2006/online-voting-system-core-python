from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
