import asyncio

import streamlit as st

from analysis.data.company_data import CompanyData

from analysis.frontend.company_overview.actions import on_watchlist_click, on_holdings_click
from analysis.frontend.company_overview.right_pane import show_right_pane
from analysis.models.company import Company
from analysis.utils import format_number

st.title("Company Overview")

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
""",
    unsafe_allow_html=True,
)

statistics, charts = st.columns([1, 4])


with statistics:
    ticker = st.text_input(
        "",
        "VERI",
    )

    if "WATCH-" + ticker not in st.session_state or st.session_state["WATCH-" + ticker] is False:
        st.button(
            "Add to watchlist",
            type="secondary",
            on_click=on_watchlist_click,
            args=(ticker,),
            use_container_width=True,
        )
    else:
        st.button(
            "Remove from watchlist",
            on_click=on_watchlist_click,
            args=(ticker,),
            use_container_width=True,
        )

    if "HOLD-" + ticker not in st.session_state or st.session_state["HOLD-" + ticker] is False:
        st.button(
            "Add to holdings",
            type="secondary",
            on_click=on_holdings_click,
            args=(ticker,),
            use_container_width=True,
        )
    else:
        st.button(
            "Remove from holdings",
            on_click=on_holdings_click,
            args=(ticker,),
            use_container_width=True,
        )

    company = asyncio.run(Company.load(ticker))
    profile = CompanyData.get_profile(company)

    st.html('<span style="color:#A7A15A;font-size:150%;">Key Metrics</span>')

    left, _ = st.columns(2)
    with left:
        st.metric("Market Cap", "$" + format_number(company.profile["mktCap"]))

    left, right = st.columns(2)
    with left:
        st.metric("P/E Ratio", str(profile["pe_ratio"]))
    with right:
        st.metric("P/B Ratio", str(profile["pb_ratio"]))

    left, right = st.columns(2)
    with left:
        st.metric("Burn Rate", "$" + str(profile["burn_rate"]))
    with right:
        st.metric("Runway (mths)", str(profile["runway"]))

    st.html('<span style="color:#A7A15A;font-size:150%;">Financials</span>')

    left, right = st.columns(2)
    with left:
        st.metric(
            "Revenue",
            "$" + format_number(company.income["revenue"].iloc[0]),
            f"{CompanyData.get_last_revenue_percentage_change(company)}%",
        )
    with right:
        st.metric("Cash", "$" + str(profile["cash"]))

    st.html('<span style="color:#A7A15A;font-size:150%;">Dates</span>')

    left, right = st.columns(2)
    with left:
        st.metric("IPO Date", company.profile["ipoDate"])
    with right:
        st.metric("Earnings", company.quote["earningsAnnouncement"][:10])


with charts:
    show_right_pane(company)
