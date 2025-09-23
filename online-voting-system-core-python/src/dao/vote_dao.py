from src.config import get_supabase

class VoteDAO:
    @staticmethod
    def has_voted(voter_id, election_id):
        supabase = get_supabase()
        response = supabase.table("vote").select("*")\
            .eq("voter_id", voter_id)\
            .eq("election_id", election_id).execute()
        return bool(response.data)

    @staticmethod
    def add_vote(voter_id, election_id, candidate_id):
        supabase = get_supabase()
        vote = {
            "voter_id": voter_id,
            "election_id": election_id,
            "candidate_id": candidate_id
        }
        supabase.table("vote").insert(vote).execute()
