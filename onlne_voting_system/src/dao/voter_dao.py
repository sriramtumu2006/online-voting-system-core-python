# src/dao/voter_dao.py
from src.config import get_supabase

class VoterDAO:
    @staticmethod
    def add_voter(name, email, password):
        supabase = get_supabase()
        supabase.table("voter").insert({
            "name": name,
            "email": email,
            "password": password
        }).execute()

    @staticmethod
    def get_voter_by_email(email):
        supabase = get_supabase()
        resp = supabase.table("voter").select("*").eq("email", email).execute()
        return resp.data[0] if resp.data else None

    @staticmethod
    def validate_login(email, password):
        supabase = get_supabase()
        resp = supabase.table("voter").select("*").eq("email", email).eq("password", password).execute()
        return resp.data[0] if resp.data else None
