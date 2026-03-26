import streamlit as st

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return   # ⭐ IMPORTANT → do not show login UI

    # ⭐ Clear page and show only login
    st.empty()

    st.markdown("## 🔐 GPU Monitoring Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if (
            username == st.secrets["USER"]
            and password == st.secrets["PASS"]
        ):
            st.session_state.logged_in = True
            #st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()   # ⭐ VERY IMPORTANT → stops dashboard rendering