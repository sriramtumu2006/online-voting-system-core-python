from src.config import get_supabase

class AdminDao:
    @staticmethod
    def add_voter(name, email, password):
        supabase = get_supabase()
        voter = {"name": name, "email": email, "password": password}
        supabase.table("voter").insert(voter).execute()
        
    def get_voter_by_email(email):
        supabase = get_supabase()
        response = supabase.table("voter").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None