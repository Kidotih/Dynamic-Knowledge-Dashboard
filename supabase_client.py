import os
import streamlit as st
from supabase import create_client

def init_connection():
    """Initialize Supabase client using either Streamlit secrets or local .env"""
    try:
        SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
        SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))

        if not SUPABASE_URL or not SUPABASE_KEY:
            st.error("❌ Supabase credentials missing. Set them in .env locally or Streamlit Secrets in deployed app.")
            return None

        print(f"✅ Using Supabase URL: {SUPABASE_URL}")
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return client

    except Exception as e:
        st.error(f"Error initializing Supabase: {e}")
        return None
