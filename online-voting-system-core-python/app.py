# app.py
import streamlit as st
from datetime import datetime, timedelta

from src.database import get_supabase_client
from src.services.admin_service import AdminService
from src.services.voter_service import VoterService
from src.services.election_service import ElectionService
from src.services.candidate_service import CandidateService
from src.services.vote_service import VoteService
from src.services.report_service import ReportService

supabase = get_supabase_client()

# --- Sidebar Navigation ---
st.sidebar.title("Online Voting System")
page = st.sidebar.selectbox("Choose Section", ["Home", "Admin", "Voter"])

# ---------------- HOME ----------------
if page == "Home":
    st.title("Welcome to the Online Voting System")
    st.write("Use the sidebar to navigate between Admin and Voter sections.")

# ---------------- ADMIN ----------------
elif page == "Admin":
    st.header("Admin Panel")

    admin_action = st.radio(
        "Choose Action",
        ["Create Election", "Add Candidate", "Force End Election", "View Reports"]
    )

    if admin_action == "Create Election":
        st.subheader("Create Election")
        title = st.text_input("Election Title")
        desc = st.text_area("Description")
        start_input = st.text_input("Start Date (YYYY-MM-DD) [leave blank for today]")
        end_input = st.text_input("End Date (YYYY-MM-DD) [leave blank for tomorrow]")

        if st.button("Create Election"):
            start_date = start_input.strip() or datetime.today().strftime("%Y-%m-%d")
            end_date = end_input.strip() or (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
            AdminService.create_election(title, desc, start_date, end_date)
            st.success(f"Election '{title}' created!")

    elif admin_action == "Add Candidate":
        st.subheader("Add Candidate")
        elections = ElectionService.list_elections()
        election_options = {f"{e['title']} (ID: {e['election_id']})": e['election_id'] for e in elections}
        selected = st.selectbox("Select Election", list(election_options.keys()))
        election_id = election_options[selected]

        name = st.text_input("Candidate Name")
        party = st.text_input("Party Name [leave blank for Independent]").strip() or "Independent"

        if st.button("Add Candidate"):
            CandidateService.add_candidate(election_id, name, party)
            st.success(f"Candidate '{name}' added to election '{selected}'")

    elif admin_action == "Force End Election":
        st.subheader("Force End Election")
        elections = ElectionService.list_elections()
        election_options = {f"{e['title']} (ID: {e['election_id']})": e['election_id'] for e in elections}
        selected = st.selectbox("Select Election to End", list(election_options.keys()))
        election_id = election_options[selected]

        if st.button("End Election"):
            AdminService.force_end_election(election_id)
            st.success(f"Election '{selected}' ended!")

    elif admin_action == "View Reports":
        st.subheader("Election Reports")
        elections = ElectionService.list_elections()
        for e in elections:
            st.write(f"Election: {e['title']} (ID: {e['election_id']})")
            results = ReportService.view_election_results(e['election_id'])
            if results:
                st.table(results)

# ---------------- VOTER ----------------
elif page == "Voter":
    st.header("Voter Panel")

    voter_action = st.radio(
        "Choose Action",
        ["Register", "Login"]
    )

    if voter_action == "Register":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            VoterService.register_voter(name, email, password)
            st.success(f"Voter '{name}' registered!")

    elif voter_action == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            voter = VoterService.login(email, password)
            if voter:
                st.success(f"Welcome, {voter['name']}!")

                # --- Voting Menu ---
                st.subheader("Voting")
                elections = ElectionService.list_elections()
                election_options = {f"{e['title']} (ID: {e['election_id']})": e['election_id'] for e in elections}
                selected = st.selectbox("Select Election", list(election_options.keys()))
                election_id = election_options[selected]

                candidates = CandidateService.list_candidates(election_id)
                if candidates:
                    candidate_options = {f"{c['name']} ({c['party']})": c['candidate_id'] for c in candidates}
                    selected_candidate = st.selectbox("Select Candidate", list(candidate_options.keys()))
                    candidate_id = candidate_options[selected_candidate]

                    if st.button("Cast Vote"):
                        VoteService.cast_vote(voter['voter_id'], election_id, candidate_id)
                        st.success("Vote cast successfully!")
                else:
                    st.info("No candidates available for this election.")

                # --- View Results ---
                if st.button("View Election Results"):
                    ReportService.view_results(election_id)
