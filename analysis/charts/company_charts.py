import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

from analysis.api.data_api import DataAPI
from analysis.models.company import Company
from analysis.utils import format_number


class CompanyCharts:

	@staticmethod
	def show_revenue_estimates(company: Company):
		dates = list(company.income["date"])
		revenue = list(company.income["revenue"])
		dates += list(company.estimates["date"])
		revenue += list(company.estimates["estimatedRevenueAvg"])

		color_discrete_sequence = ['#ec7c34'] * len(company.income)
		color_discrete_sequence += ['#609cd4'] * len(company.estimates)

		df = pd.DataFrame(
			dict(
				dates=dates,
				revenue=revenue,
				color=color_discrete_sequence
			)
		)

		print(dates)
		print(revenue)

		fig = px.bar(df, x = 'dates', y = 'revenue', color = 'color')
		fig.show()

	@staticmethod
	def show_daily_chart(company: Company):
		title = f"{company.symbol} Closing Prices"
		fig = px.line(company.daily_chart, x="date", y="adjClose", title=title)
		fig.show()

	@staticmethod
	def show_shares_float(company: Company):
		title = f"{company.symbol} Shares Float"
		fig = px.line(company.daily_shares, x="date", y="floatShares", title=title)
		fig.show()

	@staticmethod
	def show_rnd_selling(company: Company):
		fig = go.Figure(
			data=[
				go.Bar(name='R&D Expenses', x=company.income["date"], y=company.income["researchAndDevelopmentExpenses"]),
				go.Bar(name='Selling and Marketing', x=company.income["date"], y=company.income["sellingAndMarketingExpenses"]),
				go.Bar(name='Revenue', x=company.income["date"], y=company.income["revenue"]),
			],
		)

		# Change the bar mode
		fig.update_layout()
		fig.show()

	@staticmethod
	def show_simple_financials(company: Company):
		fig = go.Figure(
			data=[
				go.Bar(name='Profit', x=company.income["date"], y=company.income["netIncome"]),
				go.Bar(name='Revenue', x=company.income["date"], y=company.income["revenue"]),
				go.Bar(name='Assets', x=company.balance_sheet["date"], y=company.balance_sheet["totalAssets"]),
				go.Bar(name='Liabilities', x=company.balance_sheet["date"], y=company.balance_sheet["totalLiabilities"]),
				go.Bar(name='Debt', x=company.balance_sheet["date"], y=company.balance_sheet["netDebt"])
			],
		)

		# Change the bar mode
		fig.update_layout()
		fig.show()

	@staticmethod
	def get_peer_charts(symbol: str) -> None:
		peers = [symbol] + DataAPI.get_peers(symbol)
		prices = DataAPI.get_bulk_prices(peers)

		rows, remainder = divmod(len(peers), 2)
		if remainder == 1:
			rows += 1

		titles = [CompanyCharts.build_chart_title(price) for price in prices]
		fig = make_subplots(
			rows=rows,
			cols=2,
			subplot_titles=titles,
			vertical_spacing=0.15
		)

		for idx, peer in enumerate(peers):
			row, col = divmod(idx, 2)

			chart_df = DataAPI.get_daily_chart(peer)
			fig.add_trace(
				go.Scatter(
					x=chart_df["date"],
					y=chart_df["adjClose"]
				),
				row=row + 1,
				col=col + 1
			)

		fig.update_layout(height=400 * rows, showlegend=False)
		fig.show()

	@staticmethod
	def show_key_metrics(company: Company) -> None:
		fig = make_subplots(
			rows=1,
			cols=2,
			subplot_titles=(
				"P/E Ratio",
				"P/B Ratio",
			),
			vertical_spacing=0.15
		)
		fig.add_trace(go.Bar(x=company.ratios["date"], y=company.ratios["priceEarningsRatio"]), row=1, col=1)
		fig.add_trace(go.Bar(x=company.ratios["date"], y=company.ratios["priceToBookRatio"]), row=1, col=2)
		fig.update_layout(height=400, showlegend=False)
		fig.show()

	@staticmethod
	def show_employee_count(company: Company):
		employee_history = pd.DataFrame(DataAPI.get_employee_history(company.symbol))

		if len(employee_history):
			fig = go.Figure(
				data=[
					go.Bar(
						name='Employees',
						x=employee_history["periodOfReport"],
						y=employee_history["employeeCount"]
					),
				],
			)

			# Change the bar mode
			fig.update_layout()
			fig.show()

	@staticmethod
	def build_chart_title(quote: dict) -> str:
		market_cap = format_number(quote["marketCap"])
		pe_ratio = quote["pe"]
		symbol = quote["symbol"]
		return f"{symbol} | P/E: {pe_ratio} | Market Cap: {market_cap}"
