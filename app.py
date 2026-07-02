import streamlit as st

st.set_page_config(
    page_title="Network Latency Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Network Latency Dashboard")

st.write(
"""
Welcome!

Choose a page from the sidebar.

The first page is **Overview**, where you'll load your experiment folder once.
All other pages will automatically use the loaded data.
"""
)