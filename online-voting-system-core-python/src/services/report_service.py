from datetime import datetime
from src.dao.election_dao import ElectionDAO
from src.dao.candidate_dao import CandidateDAO

class ReportService:
    @staticmethod
    def view_election_results(election_id):
        """
        Returns a list of dicts for admin view.
        """
        election = ElectionDAO.get_election(election_id)
        if not election:
            return {"error": "Election not found."}

        results = ElectionDAO.get_results(election_id)
        total_voters = ElectionDAO.get_total_voters()
        voters_participated = ElectionDAO.get_voters_participated(election_id)

        # enrich with candidate party info
        candidates = CandidateDAO.get_candidates_by_election(election_id)
        candidate_map = {c["candidate_id"]: c for c in candidates}

        for r in results:
            cand = candidate_map.get(r["candidate_id"])
            if cand:
                r["party"] = cand.get("party", "Independent")

        return {
            "election": election,
            "results": results,
            "total_voters": total_voters,
            "voters_participated": voters_participated
        }

    @staticmethod
    def view_results_for_voter(election_id):
        """
        Returns results for voter only if election has ended.
        """
        if not ElectionDAO.has_ended(election_id):
            return {"error": "Results will be available only after the election ends."}

        results = ElectionDAO.get_results(election_id)
        if not results:
            return {"error": "No votes have been cast in this election."}

        # enrich with candidate party info
        candidates = CandidateDAO.get_candidates_by_election(election_id)
        candidate_map = {c["candidate_id"]: c for c in candidates}

        for r in results:
            cand = candidate_map.get(r["candidate_id"])
            if cand:
                r["party"] = cand.get("party", "Independent")

        # find winner
        winner = max(results, key=lambda x: x["votes"])
        return {
            "results": results,
            "winner": winner
        }
