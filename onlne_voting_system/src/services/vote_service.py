# src/services/vote_service.py
from src.config import get_supabase

class VoteService:
    @staticmethod
    def cast_vote(voter_id, election_id, candidate_id):
        supabase = get_supabase()
        # Check if already voted
        resp = supabase.table("vote").select("*").eq("voter_id", voter_id).eq("election_id", election_id).execute()
        if resp.data:
            return False
        supabase.table("vote").insert({
            "voter_id": voter_id,
            "election_id": election_id,
            "candidate_id": candidate_id
        }).execute()
        return True
