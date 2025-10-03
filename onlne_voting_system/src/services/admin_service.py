# src/services/admin_service.py
from src.services.voter_service import VoterService
from src.dao.election_dao import ElectionDAO

class AdminService:
    @staticmethod
    def register_voter(name, email, password):
        supabase = ElectionDAO.get_supabase()  # reuse get_supabase
        supabase.table("voter").insert({"name": name, "email": email, "password": password}).execute()

    @staticmethod
    def create_election(title, desc, start_date, end_date):
        ElectionDAO.add_election(title, desc, start_date, end_date)

    @staticmethod
    def force_end_election(election_id):
        ElectionDAO.end_election(election_id)
