# src/services/report_service.py
from src.dao.election_dao import ElectionDAO

class ReportService:
    @staticmethod
    def view_results_for_voter(election_id):
        if not ElectionDAO.has_ended(election_id):
            return []  # results not available yet
        return ElectionDAO.get_results(election_id)

    @staticmethod
    def view_election_results(election_id):
        return ElectionDAO.get_results(election_id)
