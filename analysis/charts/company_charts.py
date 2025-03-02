import datetime

import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots  # type: ignore

from analysis.api.company_api import CompanyAPI
from analysis.models.company import Company


class CompanyCharts:
    @staticmethod
    def get_revenue_estimates(company: Company) -> Figure:
        """
        Returns a chart showing analyst revenue estimates.
        """
        income_df = company.income[["date", "revenue"]].copy()
        estimates_df = company.estimates[["date", "estimatedRevenueAvg"]].copy()

        income_df["date"] = pd.to_datetime(income_df["date"])
        estimates_df["date"] = pd.to_datetime(estimates_df["date"])

        income_df = income_df.sort_values("date")
        estimates_df = estimates_df.sort_values("date")

        last_revenue_date = income_df.iloc[-1]["date"]
        one_week = datetime.timedelta(days=7)
        future_estimates_df = estimates_df.loc[
            estimates_df["date"] > last_revenue_date + one_week
        ]

        complete_df = pd.concat([income_df, future_estimates_df])
        fig = px.line(complete_df, x="date", y=["revenue", "estimatedRevenueAvg"])

        fig.update_layout(
            title=dict(text="Revenue (Actual & Estimates)"),
            legend=dict(
                x=0,
                y=1,
                traceorder="normal",
                font=dict(
                    size=10,
                ),
            ),
        )

        return fig

    @staticmethod
    def get_daily_chart(company: Company) -> Figure:
        """
        Returns a chart showing the adjusted closing price.
        """
        title = "Closing Prices"
        return px.line(company.daily_chart, x="date", y="adjClose", title=title)

    @staticmethod
    def get_shares_float(company: Company) -> Figure:
        """
        Returns a chart showing the number of shares circulating the public market.
        """
        title = "Shares Float"
        return px.line(company.daily_shares, x="date", y="floatShares", title=title)

    @staticmethod
    def get_rnd_selling(company: Company) -> Figure:
        """
        Returns a chart comparing expenses against revenue.
        """
        fig = go.Figure(
            data=[
                go.Bar(
                    name="R&D Expenses",
                    x=company.income["date"],
                    y=company.income["researchAndDevelopmentExpenses"],
                ),
                go.Bar(
                    name="Selling and Marketing",
                    x=company.income["date"],
                    y=company.income["sellingAndMarketingExpenses"],
                ),
                go.Bar(
                    name="Revenue",
                    x=company.income["date"],
                    y=company.income["revenue"],
                ),
            ],
        )

        # Change the bar mode
        fig.update_layout(
            title=dict(text="Revenue vs. Expenses"),
            legend=dict(
                x=0,
                y=1,
                traceorder="normal",
                font=dict(
                    size=10,
                ),
            ),
        )
        return fig

    @staticmethod
    def get_simple_financials(company: Company) -> Figure:
        """Returns a chart comparing simple financial metrics"""
        fig = go.Figure(
            data=[
                go.Bar(
                    name="Profit",
                    x=company.income["date"],
                    y=company.income["netIncome"],
                ),
                go.Bar(
                    name="Revenue",
                    x=company.income["date"],
                    y=company.income["revenue"],
                ),
                go.Bar(
                    name="Assets",
                    x=company.balance_sheet["date"],
                    y=company.balance_sheet["totalAssets"],
                ),
                go.Bar(
                    name="Liabilities",
                    x=company.balance_sheet["date"],
                    y=company.balance_sheet["totalLiabilities"],
                ),
                go.Bar(
                    name="Debt",
                    x=company.balance_sheet["date"],
                    y=company.balance_sheet["netDebt"],
                ),
            ],
        )

        # Change the bar mode
        fig.update_layout(
            title=dict(text="Income vs. Assets"),
            legend=dict(
                x=0,
                y=1,
                traceorder="normal",
                font=dict(
                    size=10,
                ),
            ),
        )
        return fig

    @staticmethod
    def get_key_metrics(company: Company) -> Figure:
        """
        Returns a chart comparing key computed metrics (e.g. P/E, P/B)
        """
        fig = make_subplots(
            rows=1,
            cols=2,
            subplot_titles=(
                "P/E Ratio",
                "P/B Ratio",
            ),
            vertical_spacing=0.15,
        )
        fig.add_trace(
            go.Bar(
                x=company.ratios["date"][:16],
                y=company.ratios["priceEarningsRatio"][:16],
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                x=company.ratios["date"][:16], y=company.ratios["priceToBookRatio"][:16]
            ),
            row=1,
            col=2,
        )
        fig.update_layout(height=400, showlegend=False)
        return fig

    @staticmethod
    def get_employee_count(company: Company):
        """
        Returns a chart showing employee count over time.
        """
        employee_history = pd.DataFrame(CompanyAPI.get_employee_history(company.symbol))

        if len(employee_history):
            fig = go.Figure(
                data=[
                    go.Bar(
                        name="Employees",
                        x=employee_history["periodOfReport"],
                        y=employee_history["employeeCount"],
                    ),
                ],
            )

            # Change the bar mode
            fig.update_layout()
            return fig
