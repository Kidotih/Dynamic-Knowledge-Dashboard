import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env (local)
load_dotenv()

# Supabase credentials: from .env or Streamlit secrets
SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")

# Stop if missing
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Supabase credentials missing. Please set them in .env or Streamlit Secrets.")
    st.stop()

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------------------------
# Login
# ------------------------
def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            result = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state["user"] = {"email": result.user.email, "id": result.user.id}
            st.success(f"Welcome back, {result.user.email}!")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")

# ------------------------
# Signup
# ------------------------
def signup():
    st.subheader("🧾 Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            st.session_state["user"] = {"email": email, "guest": False}
            st.success("✅ Account created! Check your email for verification.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Signup failed: {e}")

# ------------------------
# Guest Access
# ------------------------
def guest_access():
    st.session_state["user"] = {"guest": True}
