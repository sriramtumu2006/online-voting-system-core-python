# src/dao/candidate_dao.py
from src.config import get_supabase

class CandidateDAO:
    @staticmethod
    def add_candidate(election_id, name, party="Independent"):
        supabase = get_supabase()
        candidate = {
            "election_id": election_id,
            "name": name,
            "party": party
        }
        supabase.table("candidate").insert(candidate).execute()

    @staticmethod
    def get_candidates_by_election(election_id):
        supabase = get_supabase()
        response = supabase.table("candidate").select("*").eq("election_id", election_id).execute()
        return response.data or []
