from src.config import get_supabase
from postgrest.exceptions import APIError

class VoteService:
    @staticmethod
    def cast_vote(voter_id, election_id, candidate_id):
        supabase = get_supabase()
       
        existing = supabase.table("vote").select("*")\
            .eq("voter_id", voter_id)\
            .eq("election_id", election_id).execute()
        if existing.data:
            return False, "You have already voted in this election."
        
       
        try:
            supabase.table("vote").insert({
                "voter_id": voter_id,
                "candidate_id": candidate_id,
                "election_id": election_id
            }).execute()
            return True, "Vote cast successfully!"
        except APIError as e:
            return False, f"Error casting vote: {e}"

