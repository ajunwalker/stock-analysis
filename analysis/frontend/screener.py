import asyncio

import streamlit as st

from analysis.api.screener_api import ScreenerAPI

st.title("Screener")

mkt_cap_min, mkt_cap_max, pe_min, pe_max, pb_min, pb_max, rev_change_min = st.columns(7)

with mkt_cap_min:
    mkt_cap_min_input = st.text_input(
        "Mkt Cap Min",
        "2_000_000",
    )

with mkt_cap_max:
    mkt_cap_max_input = st.text_input(
        "Mkt Cap Max",
        "10_000_000",
    )

with pe_min:
    pe_min_input = st.text_input(
        "P/E Min",
        "-5",
    )

with pe_max:
    pe_max_input = st.text_input(
        "P/E Max",
        "5",
    )

with pb_min:
    pb_min_input = st.text_input(
        "P/B Min",
        "",
    )

with pb_max:
    pb_max_input = st.text_input(
        "P/B Max",
        "",
    )

with rev_change_min:
    rev_change_min_input = st.text_input(
        "Revenue Change Min",
        "",
    )

result = asyncio.run(
    ScreenerAPI.search(
        market_cap_more_than=int(mkt_cap_min_input)
        if mkt_cap_min_input != ""
        else None,
        market_cap_less_than=int(mkt_cap_max_input)
        if mkt_cap_max_input != ""
        else None,
        pe_ratio_less_than=int(pe_min_input) if pe_min_input != "" else None,
        pe_ratio_more_than=int(pe_max_input) if pe_max_input != "" else None,
        pb_ratio_less_than=int(pb_min_input) if pb_min_input != "" else None,
        pb_ratio_more_than=int(pb_max_input) if pb_max_input != "" else None,
        revenue_change_more_than=int(rev_change_min_input)
        if rev_change_min_input != ""
        else None,
        country="US",
        sector="Technology",
        limit=100,
    )
)

num_rows = len(result)
height = (num_rows + 1) * 35 + 3

st.dataframe(result, use_container_width=True, height=height)
