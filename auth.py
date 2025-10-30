import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

from supabase_client import init_connection

supabase = init_connection()


# Load .env for local dev
load_dotenv()

# -----------------------------------
# Lazy Supabase Client
# -----------------------------------
@st.cache_resource
def init_connection() -> Client:
    """
    Initialize Supabase connection.
    Prefers Streamlit secrets in deployed environment, falls back to .env locally.
    """
    # Try Streamlit secrets first (for deployed app)
    url = st.secrets.get("SUPABASE_URL", None)
    key = st.secrets.get("SUPABASE_KEY", None)

    # Fallback to .env (for local development)
    if not url:
        url = os.getenv("SUPABASE_URL")
    if not key:
        key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("❌ Supabase credentials missing. Set them in `.env` locally or Streamlit Secrets in deployed app.")
        st.stop()

    return create_client(url, key)


# -----------------------------------
# Authentication
# -----------------------------------
def login():
    supabase = supabase_client()
    st.subheader("🔐 Login to Your Account")
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

def signup():
    supabase = supabase_client()
    st.subheader("🧾 Create an Account")
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

def guest_access():
    """Set guest user in session."""
    st.session_state["user"] = {"guest": True}
