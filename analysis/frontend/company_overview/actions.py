import streamlit as st

from analysis.persistence.data_store import DataStore

ds = DataStore()

for symbol in ds.get_watchlist():
	st.session_state["WATCH-" + symbol] = True

for symbol in ds.get_holdings():
	st.session_state["HOLD-" + symbol] = True


def on_watchlist_click(ticker: str):
	if "WATCH-" + ticker not in st.session_state or st.session_state["WATCH-" + ticker] is False:
		st.session_state["WATCH-" + ticker] = True
		ds.save_to_watchlist(ticker)
	else:
		st.session_state["WATCH-" + ticker] = False
		ds.remove_from_watchlist(ticker)


def on_holdings_click(ticker: str):
	if "HOLD-" + ticker not in st.session_state or st.session_state["HOLD-" + ticker] is False:
		st.session_state["HOLD-" + ticker] = True
		ds.save_to_holdings(ticker)
	else:
		st.session_state["HOLD-" + ticker] = False
		ds.remove_from_holdings(ticker)
