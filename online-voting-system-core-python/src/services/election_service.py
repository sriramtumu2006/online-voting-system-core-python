from src.dao.election_dao import ElectionDAO

class ElectionService:
    @staticmethod
    def list_elections():
        elections = ElectionDAO.list_elections()
        if not elections:
            print("No elections available.")
        else:
            for e in elections:
                print(f"ID: {e['election_id']} | {e['title']} ({e['start_date']} to {e['end_date']})")
        return elections

    @staticmethod
    def get_election(election_id):
        election = ElectionDAO.get_election(election_id)
        if not election:
            print(f"Election ID {election_id} not found.")
        return election
