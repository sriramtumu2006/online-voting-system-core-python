# src/services/election_service.py
from src.dao.election_dao import ElectionDAO

class ElectionService:
    @staticmethod
    def list_elections():
        return ElectionDAO.list_elections()

    @staticmethod
    def get_election(election_id):
        return ElectionDAO.get_election(election_id)
