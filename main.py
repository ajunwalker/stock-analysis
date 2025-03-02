import streamlit as st
from dotenv import load_dotenv

st.set_page_config(layout="wide")

load_dotenv()

pg = st.navigation(
    [
        st.Page("analysis/frontend/company_overview/index.py", title="Company Overview"),
        st.Page("analysis/frontend/screener.py", title="Screener"),
        st.Page("analysis/frontend/watchlist.py", title="Watchlist"),
    ]
)
pg.run()
