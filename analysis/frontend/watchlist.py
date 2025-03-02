import asyncio

import streamlit as st

from analysis.api.screener_api import ScreenerAPI
from analysis.persistence.data_store import DataStore

st.title("Holdings & Watchlist")

ds = DataStore()
watchlist = ds.get_watchlist()
holdings = ds.get_holdings()

watchlist_profiles = asyncio.run(ScreenerAPI.populate_profiles(watchlist))
holdings_profiles = asyncio.run(ScreenerAPI.populate_profiles(holdings))

st.title("Holdings")

num_rows = len(holdings_profiles)
height = (num_rows + 1) * 35 + 3
st.dataframe(holdings_profiles, use_container_width=True, height=height)

st.title("Watchlist")

num_rows = len(watchlist_profiles)
height = (num_rows + 1) * 35 + 3
st.dataframe(watchlist_profiles, use_container_width=True, height=height)

