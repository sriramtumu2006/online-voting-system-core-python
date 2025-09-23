from src.dao.vote_dao import VoteDAO

class VoteService:
    @staticmethod
    def cast_vote(voter_id, election_id, candidate_id):
        if VoteDAO.has_voted(voter_id, election_id):
            print("You have already voted in this election.")
            return
        VoteDAO.add_vote(voter_id, election_id, candidate_id)
        print("Vote cast successfully!")
