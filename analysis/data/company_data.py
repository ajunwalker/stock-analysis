import pandas as pd

from analysis.data.templates.profile import PROFILE_TEMPLATE
from analysis.models.company import Company
from analysis.utils import format_number


class CompanyData:
    @staticmethod
    def get_percentage_change(new_value: int, old_value: int) -> float:
        change = (new_value - old_value) / old_value
        return round(change * 100, 2)

    @staticmethod
    def get_daily_change(company: Company, days: int) -> str:
        if len(company.daily_chart) > days:
            change = CompanyData.get_percentage_change(
                company.daily_chart.iloc[0]["adjClose"],
                company.daily_chart.iloc[days]["adjClose"],
            )
            return f"{change}%"
        return "N/A"

    @staticmethod
    def get_last_ratio_value(company: Company, key: str) -> float:
        if len(company.ratios) > 0:
            return round(company.ratios.iloc[0][key], 2)
        return float("-inf")

    @staticmethod
    def get_last_revenue_change(company: Company) -> str:
        if "revenue" in company.income:
            return format_number(
                company.income["revenue"].iloc[0] - company.income["revenue"].iloc[1]
            )
        return "N/A"

    @staticmethod
    def get_last_revenue_percentage_change(company: Company) -> float:
        if "revenue" in company.income:
            change = CompanyData.get_percentage_change(
                company.income["revenue"].iloc[0], company.income["revenue"].iloc[1]
            )
            return change
        return float("-inf")

    @staticmethod
    def print_profile(company: Company) -> None:
        runway = CompanyData.get_company_cash_runway(company)

        kwargs = {
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

        formatted_template = PROFILE_TEMPLATE.format(**kwargs)
        print(formatted_template)

    @staticmethod
    def get_company_cash_runway(company: Company) -> pd.DataFrame:
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
