import streamlit as st
from supabase import create_client

SUPABASE_URL = "https://qunelxtnhtzgpxiaznkf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF1bmVseHRuaHR6Z3B4aWF6bmtmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3ODI2NjgsImV4cCI6MjEwODM1ODY2OH0.lprVXnmYij-Rp0LqMnn-3wo7fWA8VI0AauNFv3RTIdY"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "user" not in st.session_state:
    st.session_state.user = None

def check_login():
    if st.session_state.user is None:
        st.title("🩺 MediTools - Login Required")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login", type="primary"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
        with tab2:
            email2 = st.text_input("New Email", key="s1")
            pass2 = st.text_input("New Password", type="password", key="s2")
            name = st.text_input("Full Name")
            if st.button("Create Account"):
                try:
                    supabase.auth.sign_up({"email": email2, "password": pass2, "options": {"data": {"full_name": name}}})
                    st.success("Account created! Please login now in Login tab.")
                except Exception as e:
                    st.error(str(e))
        st.stop() # Stop the rest of app if not logged in
