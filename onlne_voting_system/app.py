# app.py
import streamlit as st
from datetime import datetime
from src.services.voter_service import VoterService
from src.services.admin_service import AdminService
from src.services.election_service import ElectionService
from src.services.vote_service import VoteService
from src.services.candidate_service import CandidateService
from src.services.report_service import ReportService

st.set_page_config(page_title="Online Voting System")
st.title("Online Voting System")


if "voter" not in st.session_state:
    st.session_state["voter"] = None
if "voter_action" not in st.session_state:
    st.session_state["voter_action"] = "List Elections"


role = st.sidebar.selectbox("Select Role", ["Voter", "Admin"])


if role == "Voter":
    st.header("Voter Portal")


    if st.session_state["voter"] is None:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            voter = VoterService.login(email, password)
            if voter:
                st.session_state["voter"] = voter
                st.session_state["voter_action"] = "List Elections"
                st.success(f"Welcome {voter['name']}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")


    else:
        voter = st.session_state["voter"]
        st.success(f"Logged in as {voter['name']}")

        voter_action = st.selectbox(
            "Choose Action",
            ["List Elections", "Cast Vote", "View Results", "Logout"],
            index=["List Elections", "Cast Vote", "View Results", "Logout"].index(st.session_state["voter_action"])
        )
        st.session_state["voter_action"] = voter_action


        if voter_action == "List Elections":
            elections = ElectionService.list_elections()
            if elections:
                st.subheader("Available Elections")
                for e in elections:
                    st.write(f"ID: {e['election_id']} | {e['title']} | Status: {e.get('status', 'N/A')}")
            else:
                st.info("No elections available.")


        elif voter_action == "Cast Vote":
            elections = ElectionService.list_elections()
            if elections:
                election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
                selected = st.selectbox("Select Election", list(election_options.keys()))
                election_id = election_options[selected]

                candidates = CandidateService.list_candidates(election_id)
                election = next((e for e in elections if e['election_id'] == election_id), None)
                if election and election.get("status", "").lower() == "ended":
                    st.warning("This election has already ended. You cannot vote now.")
                else:
                    if candidates:
                        candidate_options = {f"{c['name']} ({c.get('party','Independent')})": c['candidate_id'] for c in candidates}
                        selected_candidate = st.selectbox("Select Candidate", list(candidate_options.keys()))
                        candidate_id = candidate_options[selected_candidate]

                        if st.button("Vote"):
                            VoteService.cast_vote(voter['voter_id'], election_id, candidate_id)
                            st.success("Vote cast successfully!")
                        else:
                            st.warning("No candidates available for this election.")
                    else:
                    st.warning("No candidates available for this election.")


        elif voter_action == "View Results":
            elections = ElectionService.list_elections()
            if elections:
                election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
                selected = st.selectbox("Select Election", list(election_options.keys()))
                election_id = election_options[selected]

                st.subheader("Election Results")
                results = ReportService.view_results_for_voter(election_id)
                if results:
                    for r in results:
                        st.write(f"{r['candidate_name']} ({r.get('party','Independent')}) - {r['votes']} votes")
                else:
                    st.info("Results will be available only after the election ends.")
            else:
                st.info("No elections available.")

        elif voter_action == "Logout":
            st.info("Are you sure you want to logout?")
            if st.button("Confirm Logout"):
                st.session_state.clear()
                st.success("You have been logged out successfully.")
                st.rerun()


elif role == "Admin":
    st.header("Admin Portal")
    action = st.selectbox(
        "Choose Action",
        ["Register Voter", "Create Election", "Add Candidate", "View Reports", "Force End Election"]
    )

    if action == "Register Voter":
        name = st.text_input("Voter Name")
        email = st.text_input("Voter Email")
        password = st.text_input("Voter Password", type="password")
        if st.button("Register Voter"):
            AdminService.register_voter(name, email, password)
            st.success(f"Voter {name} registered!")

    elif action == "Create Election":
        title = st.text_input("Election Title")
        desc = st.text_input("Description")
        start_date = st.date_input("Start Date", datetime.today())
        end_date = st.date_input("End Date", datetime.today())
        if st.button("Create Election"):
            AdminService.create_election(title, desc, start_date.isoformat(), end_date.isoformat())
            st.success(f"Election '{title}' created!")

    elif action == "Add Candidate":
        elections = ElectionService.list_elections()
        if elections:
            election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
            selected = st.selectbox("Select Election", list(election_options.keys()))
            election_id = election_options[selected]

            name = st.text_input("Candidate Name")
            party = st.text_input("Party Name (leave blank for Independent)")
            if st.button("Add Candidate"):
                party = party.strip() or "Independent"
                CandidateService.add_candidate(election_id, name, party)
                st.success(f"Candidate '{name}' added to election {election_id}")
        else:
            st.info("No elections available to add candidates.")

    elif action == "View Reports":
        elections = ElectionService.list_elections()
        if elections:
            election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
            selected = st.selectbox("Select Election", list(election_options.keys()))
            election_id = election_options[selected]

            st.subheader("Election Results")
            results = ReportService.view_election_results(election_id)
            if results:
                for r in results:
                    st.write(f"{r['candidate_name']} ({r.get('party','Independent')}) - {r['votes']} votes")
            else:
                st.info("No votes have been cast yet.")
        else:
            st.info("No elections available.")

    elif action == "Force End Election":
        elections = ElectionService.list_elections()
        if elections:
            election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
            selected = st.selectbox("Select Election", list(election_options.keys()))
            election_id = election_options[selected]
            if st.button("End Election"):
                AdminService.force_end_election(election_id)
                st.success(f"Election {election_id} ended!")
        else:
            st.info("No elections available to end.")




