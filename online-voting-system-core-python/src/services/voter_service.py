from src.dao.voter_dao import VoterDAO

class VoterService:
    @staticmethod
    def login(email, password):
        voter = VoterDAO.authenticate(email, password)
        if voter:
            print(f"Welcome, {voter['name']}!")
            return voter
        print("Invalid credentials.")
        return None
