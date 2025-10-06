# src/services/election_service.py
from src.dao.election_dao import ElectionDAO

class ElectionService:
    @staticmethod
    def list_elections():
        elections = election_dao.list_elections()
        ElectionService.auto_end_elections(elections)
        return elections

    @staticmethod
    def get_election(election_id):
        return ElectionDAO.get_election(election_id)

 @staticmethod
    def auto_end_elections(elections):
        """Automatically end elections whose end_date has passed."""
        today = date.today()
        for election in elections:
            if election.get("status", "").lower() != "ended":
                try:
                    end_date = date.fromisoformat(str(election["end_date"]))
                    if today > end_date:
                        election_dao.update_status(election["election_id"], "Ended")
                except Exception as e:
                    print(f"Error auto-ending election {election['election_id']}: {e}")
