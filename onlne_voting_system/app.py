# app.py
import streamlit as st
from datetime import datetime
from src.services.voter_service import VoterService
from src.services.admin_service import AdminService
from src.services.election_service import ElectionService
from src.services.vote_service import VoteService
from src.services.candidate_service import CandidateService
from src.services.report_service import ReportService

st.title("🌐 Online Voting System")

role = st.sidebar.selectbox("Select Role", ["Voter", "Admin"])

# ----------------- VOTER -----------------
if role == "Voter":
    st.header("Voter Portal")

    action = st.selectbox("Choose Action", ["Login", "Back"], key="voter_action")
    if action == "Login":
        email = st.text_input("Email", key="voter_email")
        password = st.text_input("Password", type="password", key="voter_password")
        if st.button("Login", key="voter_login"):
            voter = VoterService.login(email, password)
            if voter:
                st.success(f"Welcome {voter['name']}!")

                voter_action = st.selectbox(
                    "Choose Action", 
                    ["List Elections", "Cast Vote", "View Results"], 
                    key="voter_action2"
                )

                # List Elections
                if voter_action == "List Elections":
                    elections = ElectionService.list_elections()
                    if elections:
                        st.subheader("Available Elections")
                        for e in elections:
                            st.write(f"ID: {e['election_id']} | {e['title']} | Status: {e.get('status', 'N/A')}")
                    else:
                        st.info("No elections available.")

                # Cast Vote
                elif voter_action == "Cast Vote":
                    elections = ElectionService.list_elections()
                    if elections:
                        election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
                        selected = st.selectbox("Select Election", list(election_options.keys()), key="voter_election")
                        election_id = election_options[selected]

                        candidates = CandidateService.list_candidates(election_id)
                        if candidates:
                            candidate_options = {f"{c['name']} ({c.get('party','Independent')})": c['candidate_id'] for c in candidates}
                            selected_candidate = st.selectbox("Select Candidate", list(candidate_options.keys()), key="voter_candidate")
                            candidate_id = candidate_options[selected_candidate]

                            if st.button("Vote", key="vote_button"):
                                VoteService.cast_vote(voter['voter_id'], election_id, candidate_id)
                                st.success("Vote cast successfully!")
                        else:
                            st.warning("No candidates available for this election.")
                    else:
                        st.info("No elections available.")

                # View Results
                elif voter_action == "View Results":
                    elections = ElectionService.list_elections()
                    if elections:
                        election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
                        selected = st.selectbox("Select Election", list(election_options.keys()), key="voter_result_election")
                        election_id = election_options[selected]

                        st.subheader("Results")
                        results = ReportService.view_results_for_voter(election_id)
                        if results:
                            for r in results:
                                st.write(f"{r['candidate_name']} - {r['votes']} votes")
                        else:
                            st.info("Results will be available after the election ends.")
                    else:
                        st.info("No elections available.")
            else:
                st.error("Invalid credentials.")

# ----------------- ADMIN -----------------
elif role == "Admin":
    st.header("Admin Portal")

    action = st.selectbox(
        "Choose Action",
        ["Register Voter", "Create Election", "Add Candidate", "View Reports", "Force End Election"],
        key="admin_action"
    )

    if action == "Register Voter":
        name = st.text_input("Voter Name", key="admin_voter_name")
        email = st.text_input("Voter Email", key="admin_voter_email")
        password = st.text_input("Voter Password", type="password", key="admin_voter_password")
        if st.button("Register Voter", key="admin_register_voter"):
            AdminService.register_voter(name, email, password)
            st.success(f"Voter {name} registered!")

    elif action == "Create Election":
        title = st.text_input("Election Title", key="admin_election_title")
        desc = st.text_input("Description", key="admin_election_desc")
        start_date = st.date_input("Start Date", datetime.today(), key="admin_start_date")
        end_date = st.date_input("End Date", datetime.today(), key="admin_end_date")
        if st.button("Create Election", key="admin_create_election"):
            AdminService.create_election(title, desc, start_date.isoformat(), end_date.isoformat())
            st.success(f"Election '{title}' created!")

    elif action == "Add Candidate":
        elections = ElectionService.list_elections()
        if elections:
            election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
            selected = st.selectbox("Select Election", list(election_options.keys()), key="admin_election_select")
            election_id = election_options[selected]

            name = st.text_input("Candidate Name", key="admin_candidate_name")
            party = st.text_input("Party Name (leave blank for Independent)", key="admin_candidate_party")
            if st.button("Add Candidate", key="admin_add_candidate"):
                party = party.strip() or "Independent"
                CandidateService.add_candidate(election_id, name, party)
                st.success(f"Candidate '{name}' added to election {election_id}")
        else:
            st.info("No elections available.")

    elif action == "View Reports":
        elections = ElectionService.list_elections()
        if elections:
            election_options = {f"{e['title']} (ID:{e['election_id']})": e['election_id'] for e in elections}
            selected = st.selectbox("Select Election", list(election_options.keys()), key="admin_report_select")
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
            selected = st.selectbox("Select Election", list(election_options.keys()), key="admin_end_select")
            election_id = election_options[selected]

            if st.button("End Election", key="admin_force_end"):
                AdminService.force_end_election(election_id)
                st.success(f"Election {election_id} ended!")
        else:
            st.info("No elections available.")
