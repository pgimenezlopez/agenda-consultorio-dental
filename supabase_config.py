from supabase import create_client
import streamlit as st
from supabase._sync.client import SyncClient

url = st.secrets["supabase_url"]
key = st.secrets["supabase_key"]

supabase: SyncClient = create_client(url, key)
