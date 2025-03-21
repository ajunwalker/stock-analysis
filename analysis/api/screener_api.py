import asyncio
import datetime
from typing import Optional

import fmpsdk  # type: ignore
import pandas as pd

from analysis.api.base_api import BaseAPI
from analysis.data.company_data import CompanyData
from analysis.models.company import Company
from analysis.utils import format_number


class ScreenerAPI(BaseAPI):
    @staticmethod
    async def get_company_profiles(symbols: list[str]):
        """
        Builds a details company profile for a given list of ticker symbols.
        """
        tasks = [Company.load(symbol) for symbol in symbols]
        profiles: list[Company] = list(await asyncio.gather(*tasks))

        compiled = []
        for company in profiles:
            if company.quote["earningsAnnouncement"]:
                earnings = company.quote["earningsAnnouncement"][:10]
            else:
                earnings = "N/A"
            compiled.append(
                {
                    "Symbol": company.profile["symbol"],
                    "Name": company.profile["companyName"],
                    "Cap": "$" + format_number(company.profile["mktCap"]),
                    "IPO Date": company.profile["ipoDate"],
                    "Employees": company.profile["fullTimeEmployees"],
                    "1 Week Change": CompanyData.get_daily_change(company, 5),
                    "1 Month Change": CompanyData.get_daily_change(company, 20),
                    "3 Month Change": CompanyData.get_daily_change(company, 60),
                    "Revenue Change": CompanyData.get_last_revenue_change(company),
                    "Revenue Change (%)": CompanyData.get_last_revenue_percentage_change(
                        company
                    ),
                    "P/E": CompanyData.get_last_ratio_value(
                        company, "priceEarningsRatio"
                    ),
                    "P/B": CompanyData.get_last_ratio_value(
                        company, "priceToBookRatio"
                    ),
                    "Earnings": earnings,
                }
            )

        return compiled

    @staticmethod
    async def populate_profiles(symbols: list[str]):
        """Builds a dataframe containing the profile of all provided tickers."""
        if len(symbols) == 0:
            return pd.DataFrame()

        responses = []

        window = 10
        for idx in range(0, len(symbols), window):
            response = await ScreenerAPI.get_company_profiles(
                symbols[idx: idx + window]
            )
            responses.extend(response)

        profiles_df = pd.DataFrame(responses)
        profiles_df.set_index("Symbol", inplace=True)

        return profiles_df

    @staticmethod
    async def search(
        market_cap_more_than: Optional[int] = None,
        market_cap_less_than: Optional[int] = None,
        pe_ratio_more_than: Optional[float] = None,
        pe_ratio_less_than: Optional[float] = None,
        pb_ratio_more_than: Optional[float] = None,
        pb_ratio_less_than: Optional[float] = None,
        revenue_change_more_than: Optional[float] = None,
        country: Optional[str] = None,
        sector: Optional[str] = None,
        industry: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        Searches for a list of stocks matching the provided criteria.

        :param market_cap_more_than: Market capitalization is more than
        :param market_cap_less_than: Market capitalization is less than
        :param pe_ratio_more_than: Price-to-Earnings ratio is more than
        :param pe_ratio_less_than: Price-to-Earnings ratio is less than
        :param pb_ratio_more_than: Price-to-Book ratio is more than
        :param pb_ratio_less_than: Price-to-Book ratio is less than
        :param revenue_change_more_than: Revenue change percentage over last two quarters is more than
        :param country: Exchange country
        :param sector: Company sector
        :param industry: Company industry
        :param limit: Number of results to return
        :return: Results that match the query
        """
        result = fmpsdk.stock_screener(
            apikey=BaseAPI._get_api_key(),
            market_cap_lower_than=market_cap_less_than,
            market_cap_more_than=market_cap_more_than,
            is_etf=False,
            is_actively_trading=True,
            country=country,
            sector=sector,
            industry=industry,
            limit=limit,
        )

        if len(result) == 0:
            return pd.DataFrame()

        print(result)

        df = pd.DataFrame(result)
        df = df.loc[df["exchangeShortName"].isin(["NASDAQ", "AMEX", "NYSE"])]
        symbols = list(df["symbol"])

        responses = []

        window = 10
        for idx in range(0, len(symbols), window):
            response = await ScreenerAPI.get_company_profiles(
                symbols[idx: idx + window]
            )
            responses.extend(response)

        profiles_df = pd.DataFrame(responses)
        date_before = (
            datetime.date.today() - datetime.timedelta(days=7 * 52 * 5)
        ).strftime("%Y-%m-%d")
        profiles_df = profiles_df.loc[profiles_df["IPO Date"] > date_before]

        if pe_ratio_more_than:
            profiles_df = profiles_df.loc[profiles_df["P/E"] > pe_ratio_more_than]
        if pe_ratio_less_than:
            profiles_df = profiles_df.loc[profiles_df["P/E"] < pe_ratio_less_than]
        if pb_ratio_more_than:
            profiles_df = profiles_df.loc[profiles_df["P/B"] > pb_ratio_more_than]
        if pb_ratio_less_than:
            profiles_df = profiles_df.loc[profiles_df["P/B"] < pb_ratio_less_than]
        if revenue_change_more_than:
            profiles_df = profiles_df.loc[
                profiles_df["Revenue Change (%)"] > revenue_change_more_than
            ]

        profiles_df.set_index("Symbol")

        return profiles_df
