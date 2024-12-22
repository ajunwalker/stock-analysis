import asyncio

import pandas as pd

from analysis.api.company_api import CompanyAPI


class Company:
    symbol: str
    balance_sheet: pd.DataFrame
    income: pd.DataFrame
    cashflow: pd.DataFrame
    daily_chart: pd.DataFrame
    daily_shares: pd.DataFrame
    ratios: pd.DataFrame
    quote: dict
    profile: dict
    estimates: pd.DataFrame

    def __init__(
        self,
        symbol: str,
        balance_sheet: pd.DataFrame,
        income: pd.DataFrame,
        cashflow: pd.DataFrame,
        daily_chart: pd.DataFrame,
        daily_shares: pd.DataFrame,
        ratios: pd.DataFrame,
        quote: dict,
        profile: dict,
        estimates: pd.DataFrame,
    ):
        self.symbol = symbol
        self.balance_sheet = balance_sheet
        self.income = income
        self.cashflow = cashflow
        self.daily_chart = daily_chart
        self.daily_shares = daily_shares
        self.ratios = ratios
        self.quote = quote
        self.profile = profile
        self.estimates = estimates

    @classmethod
    async def load(cls, symbol: str) -> "Company":
        tasks = [
            CompanyAPI.get_balance_sheet_statements(symbol),
            CompanyAPI.get_income_statements(symbol),
            CompanyAPI.get_cash_flow_statements(symbol),
            CompanyAPI.get_daily_chart(symbol),
            CompanyAPI.get_daily_shares(symbol),
            CompanyAPI.get_ratios(symbol),
            CompanyAPI.get_full_quote(symbol),
            CompanyAPI.get_company_profile(symbol),
            CompanyAPI.get_analyst_estimates(symbol),
        ]

        return cls(symbol, *(await asyncio.gather(*tasks)))  # type: ignore
