import streamlit as st

def login():

    USER = st.secrets.get("USER", "admin")
    PASS = st.secrets.get("PASS", "gpu123")

    if "auth" not in st.session_state:
        st.session_state.auth = False

    if not st.session_state.auth:

        st.title("🔐 GPU Monitor Login")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):

            if u == USER and p == PASS:
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.stop()
