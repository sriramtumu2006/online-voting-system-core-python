from src.dao.candidate_dao import CandidateDAO

class CandidateService:
    @staticmethod
    def add_candidate(election_id, name, party="Independent"):
        CandidateDAO.add_candidate(election_id, name, party)
        
    def list_candidates(election_id):
        return CandidateDAO.get_candidates_by_election(election_id)