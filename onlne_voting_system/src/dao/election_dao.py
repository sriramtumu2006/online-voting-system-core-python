# src/dao/election_dao.py
from src.config import get_supabase
from datetime import datetime, timedelta

class ElectionDAO:
    @staticmethod
    def add_election(title, description, start_date=None, end_date=None):
        supabase = get_supabase()
        if not start_date:
            start_date = datetime.today().strftime("%Y-%m-%d")
        if not end_date:
            end_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        election = {
            "title": title,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "status": "ongoing"
        }
        supabase.table("election").insert(election).execute()

    @staticmethod
    def list_elections():
        supabase = get_supabase()
        response = supabase.table("election").select("*").execute()
        return response.data or []

    @staticmethod
    def get_election(election_id):
        supabase = get_supabase()
        response = supabase.table("election").select("*").eq("election_id", election_id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    def get_results(election_id):
        supabase = get_supabase()
        votes_response = supabase.table("vote").select("*").eq("election_id", election_id).execute()
        votes = votes_response.data or []

        results = {}
        for vote in votes:
            cid = vote["candidate_id"]
            results[cid] = results.get(cid, 0) + 1

        candidate_ids = list(results.keys())
        if candidate_ids:
            candidate_response = supabase.table("candidate").select("*").in_("candidate_id", candidate_ids).execute()
            candidates = {c["candidate_id"]: {"name": c["name"], "party": c.get("party", "Independent")} for c in candidate_response.data}
        else:
            candidates = {}

        formatted_results = []
        for cid, count in results.items():
            formatted_results.append({
                "candidate_id": cid,
                "candidate_name": candidates.get(cid, {}).get("name", "Unknown"),
                "party": candidates.get(cid, {}).get("party", "Independent"),
                "votes": count
            })
        return formatted_results

    @staticmethod
    def get_total_voters():
        supabase = get_supabase()
        response = supabase.table("voter").select("voter_id", count="exact").execute()
        return response.count

    @staticmethod
    def get_voters_participated(election_id):
        supabase = get_supabase()
        response = supabase.table("vote").select("voter_id", count="exact").eq("election_id", election_id).execute()
        return response.count

    @staticmethod
    def has_ended(election_id):
        election = ElectionDAO.get_election(election_id)
        if not election:
            return False
        end_date = datetime.fromisoformat(election["end_date"])
        return datetime.now() > end_date

    @staticmethod
    def end_election(election_id):
        supabase = get_supabase()
        now = datetime.now().isoformat()
        supabase.table("election").update({"end_date": now, "status": "ended"}).eq("election_id", election_id).execute()
        print(f"Election ID {election_id} has been forcefully ended.")
