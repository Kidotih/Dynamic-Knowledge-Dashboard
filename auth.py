import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# -----------------------------------
# Load environment variables from .env
# -----------------------------------
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# -----------------------------------
# Initialize Supabase client
# -----------------------------------
@st.cache_resource
def init_connection() -> Client:
    """
    Initialize Supabase connection.
    Prefers Streamlit secrets in deployed environment, falls back to .env locally.
    """
    # First try Streamlit secrets (deployed environment)
    url = st.secrets.get("SUPABASE_URL", None)
    key = st.secrets.get("SUPABASE_KEY", None)

    # Fallback to .env locally
    if not url:
        url = os.getenv("SUPABASE_URL")
    if not key:
        key = os.getenv("SUPABASE_KEY")

    # Debug info
    st.write("DEBUG: SUPABASE_URL =", url)
    st.write("DEBUG: SUPABASE_KEY =", "<hidden>" if key else None)

    if not url or not key:
        st.error("❌ Supabase credentials missing. Set them in `.env` locally or Streamlit Secrets in deployed app.")
        st.stop()

    return create_client(url, key)

# Initialize Supabase client
supabase = init_connection()


# -----------------------------------
# Authentication: Login
# -----------------------------------
def login():
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


# -----------------------------------
# Authentication: Signup
# -----------------------------------
def signup():
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


# -----------------------------------
# Guest Access
# -----------------------------------
def guest_access():
    """Set a guest user in session."""
    st.session_state["user"] = {"guest": True}
