import pandas as pd

from analysis.data.templates.profile import PROFILE_TEMPLATE
from analysis.models.company import Company
from analysis.utils import format_number


class CompanyData:
    @staticmethod
    def get_percentage_change(new_value: int, old_value: int) -> float:
        """
        Calculates the percentage change between two numbers.
        """
        change = (new_value - old_value) / old_value
        return round(change * 100, 2)

    @staticmethod
    def get_daily_change(company: Company, days: int) -> str:
        """
        Returns the percentage change in adjusted close price over a certain number of days.
        If there isn't enough data, N/A will be returned.
        """
        if (
            len(company.daily_chart) > days
            and company.daily_chart.iloc[days]["adjClose"] != 0
        ):
            change = CompanyData.get_percentage_change(
                company.daily_chart.iloc[0]["adjClose"],
                company.daily_chart.iloc[days]["adjClose"],
            )
            return f"{change}%"
        return "N/A"

    @staticmethod
    def get_last_ratio_value(company: Company, key: str) -> float:
        """
        Returns a rounded ratio.
        """
        if len(company.ratios) > 0:
            return round(company.ratios.iloc[0][key], 2)
        return float("-inf")

    @staticmethod
    def get_last_revenue_change(company: Company) -> str:
        """
        Returns the change between last two company revenues in dollar amount.
        """
        if "revenue" in company.income:
            return format_number(
                company.income["revenue"].iloc[0] - company.income["revenue"].iloc[1]
            )
        return "N/A"

    @staticmethod
    def get_last_revenue_percentage_change(company: Company) -> float:
        """
        Returns the change between last two company revenues as a percentage.
        """
        if (
            "revenue" in company.income
            and len(company.income["revenue"]) > 1
            and company.income["revenue"].iloc[1] != 0
        ):
            change = CompanyData.get_percentage_change(
                company.income["revenue"].iloc[0], company.income["revenue"].iloc[1]
            )
            return change
        return float("-inf")

    @staticmethod
    def get_profile(company: Company) -> dict:
        """
        Returns a company's complete profile in a dictionary.
        """
        runway = CompanyData.get_company_cash_runway(company)

        return {
            "company_name": company.profile["companyName"],
            "address": company.profile["address"],
            "city": company.profile["city"],
            "state": company.profile["state"],
            "sector": company.profile["sector"],
            "industry": company.profile["industry"],
            "website": company.profile["website"],
            "ipo_date": company.profile["ipoDate"],
            "pe_ratio": round(company.ratios.iloc[0]["priceEarningsRatio"], 2),
            "pb_ratio": round(company.ratios.iloc[0]["priceToBookRatio"], 2),
            "cash": format_number(
                company.balance_sheet.iloc[0]["cashAndCashEquivalents"]
            ),
            "burn_rate": format_number(runway.iloc[0]["3 Month Burn Rate"]),
            "runway": format_number(runway.iloc[0]["3 Month Average Runway"]),
            "description": company.profile["description"],
        }

    @staticmethod
    def print_profile(company: Company) -> None:
        """
        Prints the company profile in human-readable format.
        """
        kwargs = CompanyData.get_profile(company)
        print(PROFILE_TEMPLATE.format(**kwargs))

    @staticmethod
    def get_company_cash_runway(company: Company) -> pd.DataFrame:
        """
        Calculates and returns the company runway based on:
            1. How much cash they had on their last balance sheet
            2. Free cashflow (or lack thereof)

        Two different values are calculated as part of this:
            1. 12-month average burn rate (could be less accurate depending on recent changes)
            2. 3-month average burn rate (could be less accurate depending on seasonal fluctuations)

        A positive value does not mean anything, as more cash is flowing in as opposed to flowing out.
        """
        results = []

        min_len = min(len(company.balance_sheet), len(company.cashflow))
        for idx1 in range(min_len - 3):
            trailing_free_cashflow = 0

            for idx2 in range(4):
                trailing_free_cashflow += company.cashflow.iloc[idx1 + idx2][
                    "freeCashFlow"
                ]

            cash = company.balance_sheet.iloc[idx1]["cashAndCashEquivalents"]

            burn_rate = trailing_free_cashflow / 12
            last_quarter_burn_rate = company.cashflow.iloc[idx1]["freeCashFlow"] / 3

            results.append(
                {
                    "12 Month Average Runway": cash / burn_rate,
                    "12 Month Burn Rate": burn_rate,
                    "3 Month Average Runway": cash / last_quarter_burn_rate,
                    "3 Month Burn Rate": last_quarter_burn_rate,
                }
            )

        return pd.DataFrame(results)
