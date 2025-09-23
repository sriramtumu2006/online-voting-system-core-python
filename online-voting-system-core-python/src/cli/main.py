from src.services.voter_service import VoterService
from src.services.admin_service import AdminService
from src.services.election_service import ElectionService
from src.services.vote_service import VoteService
from src.services.candidate_service import CandidateService
from src.services.report_service import ReportService
from datetime import datetime, timedelta

def main_menu():
    while True:
        print("\n=== Online Voting System ===")
        print("1. Voter")
        print("2. Admin")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            voter_menu()
        elif choice == "2":
            admin_menu()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
            
def voter_menu():
    while True:
        print("\n=== Voter Menu ===")
        print("1. Login")
        print("2. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == "1":
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            voter = VoterService.login(email, password)
            if voter:
                vote_menu(voter)
        elif choice == "2":
            break
        else:
            print("Invalid choice.")
            
def vote_menu(voter):
    while True:
        print("\n=== Voting Menu ===")
        print("1. List Elections")
        print("2. Cast Vote")
        print("3. View Results")
        print("4. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            elections = ElectionService.list_elections()
            for e in elections:
                print(f"ID: {e['election_id']} --- Title: {e['title']} --- Status: {e.get('status', 'N/A')}")
        elif choice == "2":
            elections = ElectionService.list_elections()
            if not elections:
                print("No elections available.")
                continue
            print("\nAvailable Elections:")
            for e in elections:
                print(f"ID: {e['election_id']} --- Title: {e['title']}")

            election_id = input("Enter Election ID to vote: ")
            election = ElectionService.get_election(election_id)
            if not election:
                print("Invalid election ID.")
                continue
            candidates = CandidateService.list_candidates(election_id)
            if not candidates:
                print("No candidates for this election.")
                continue
            print("\nCandidates:")
            for c in candidates:
                print(f"ID: {c['candidate_id']} --- Name: {c['name']}")
            candidate_id = input("Enter Candidate ID to vote for: ")
            success = VoteService.cast_vote(voter['voter_id'], election_id, candidate_id)
            if success:
                print("Vote cast successfully!")
            else:
                print("You have already voted or an error occurred.")
        elif choice == "3":
            AdminService.view_reports()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
            
def admin_menu():
    while True:
        print("\n=== Admin Menu ===")
        print("1. Register Voter")
        print("2. Create Election")
        print("3. Add Candidate")
        print("4. View Reports / Results")
        print("5. End Election")
        print("6. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == "1":
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            AdminService.register_voter(name, email, password)
        elif choice == "2":
            title = input("Enter Election Title: ")
            desc = input("Enter Description: ")
            start_date = (input("Enter Start Date (YYYY-MM-DD) [leave blank for today]: ").strip() or datetime.today().strftime("%Y-%m-%d"))
            end_date = (input("Enter End Date (YYYY-MM-DD) [leave blank for tomorrow]: ").strip()  or (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
            AdminService.create_election(title, desc, start_date, end_date)
        elif choice == "3":
            elections = ElectionService.list_elections()
            for e in elections:
                print(f"ID: {e['election_id']} --- Title: {e['title']}")
            election_id = input("Enter Election ID to add candidate: ")
            name = input("Enter Candidate Name: ")
            party = input("Enter Party Name [leave blank for Independent]: ").strip() or "Independent"
            CandidateService.add_candidate(election_id, name,party)
            print(f"Candidate '{name}' added to election {election_id}")
        elif choice == "4":
            elections = ElectionService.list_elections()
            for e in elections:
                print(f"ID: {e['election_id']} --- Title: {e['title']}")
            election_id = input("Enter Election ID to view results: ")
            ReportService.view_results(election_id)
        elif choice == "5":
            elections = ElectionService.list_elections()
            for e in elections:
                print(f"ID: {e['election_id']} --- Title: {e['title']}")
            election_id = int(input("Enter Election ID to forcefully end: "))
            AdminService.force_end_election(election_id)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")
            
if __name__ == "__main__":
    main_menu()
