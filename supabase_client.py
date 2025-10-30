# supabase_client.py
import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def init_supabase() -> Client:
    """Initialize Supabase connection (from .env or Streamlit secrets)."""
    url = SUPABASE_URL or st.secrets.get("SUPABASE_URL")
    key = SUPABASE_KEY or st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        st.error("❌ Supabase credentials missing. Please set them in .env or Streamlit Secrets.")
        st.stop()

    return create_client(url, key)

# Initialize globally
supabase = init_supabase()
