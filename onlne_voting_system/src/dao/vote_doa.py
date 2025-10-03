# src/dao/vote_dao.py
from src.config import get_supabase

class VoteDAO:
    @staticmethod
    def has_voted(voter_id, election_id):
        supabase = get_supabase()
        resp = supabase.table("vote").select("*").eq("voter_id", voter_id).eq("election_id", election_id).execute()
        return bool(resp.data)

    @staticmethod
    def add_vote(voter_id, election_id, candidate_id):
        supabase = get_supabase()
        supabase.table("vote").insert({
            "voter_id": voter_id,
            "election_id": election_id,
            "candidate_id": candidate_id
        }).execute()
