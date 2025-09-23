from datetime import datetime
from src.dao.election_dao import ElectionDAO

class ReportService:
    @staticmethod
    def view_election_results(election_id):
        election = ElectionDAO.get_election(election_id)
        if not election:
            print("Election not found.")
            return
        start = datetime.fromisoformat(election['start_date']).date()
        end = datetime.fromisoformat(election['end_date']).date()
        print(f"Election: {election['title']} ({start} to {end})")
        results = ElectionDAO.get_results(election_id)
        if not results:
            print("No votes cast yet.")
            return
        for res in results:
            print(f"Candidate: {res['candidate_name']} | Votes: {res['votes']}")
        total_voters = ElectionDAO.get_total_voters()
        voters_participated = ElectionDAO.get_voters_participated(election_id)
        print(f"Total Voters: {total_voters}")
        print(f"Voters Participated: {voters_participated}")

    def view_results(election_id):
        if not ElectionDAO.has_ended(election_id):
            print("Results will be available only after the election ends.")
            return
        results = ElectionDAO.get_results(election_id)
        if not results:
            print("No votes have been cast in this election.")
            return
        print(f"Results for Election ID {election_id}:")
        for r in results:
            print(f"{r['candidate_name']} - {r['votes']} votes")
        winner = max(results, key=lambda x: x["votes"])
        print(f"\nWinner: {winner['candidate_name']} with {winner['votes']} votes")