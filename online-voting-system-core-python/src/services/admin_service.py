from src.dao.election_dao import ElectionDAO
from src.dao.admin_dao import AdminDao
from src.services.report_service import ReportService

class AdminService:
    @staticmethod
    def create_election(title, description, start_date, end_date):
        ElectionDAO.add_election(title, description, start_date, end_date)
        print("Election created successfully!")

    @staticmethod
    def view_reports():
        elections = ElectionDAO.list_elections()
        if not elections:
            print("No elections found.")
            return
        for e in elections:
            ReportService.view_election_results(e['election_id'])

    def force_end_election(election_id):
        election = ElectionDAO.get_election(election_id)
        if not election:
            print("Election not found.")
            return
        ElectionDAO.end_election(election_id)
        
    def register_voter(name, email, password):
        if AdminDao.get_voter_by_email(email):
            print("Email already registered.")
            return
        AdminDao.add_voter(name, email, password)
        print("Voter registered successfully!")
