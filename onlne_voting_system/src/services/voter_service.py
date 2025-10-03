# src/services/voter_service.py
from src.config import get_supabase

class VoterService:
    @staticmethod
    def login(email, password):
        supabase = get_supabase()
        resp = supabase.table("voter").select("*").eq("email", email).eq("password", password).execute()
        return resp.data[0] if resp.data else None
