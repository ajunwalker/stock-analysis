from analysis.charts.company_charts import CompanyCharts

import streamlit as st

from analysis.models.company import Company


def show_right_pane(company: Company):
	col1, col2 = st.columns(2)
	col3, col4 = st.columns(2)
	col5, _ = st.columns(2)

	# Create and display charts in each column
	with col1:
		chart = CompanyCharts.get_daily_chart(company)
		st.plotly_chart(chart, use_container_width=True)

	with col2:
		chart = CompanyCharts.get_shares_float(company)
		st.plotly_chart(chart, use_container_width=True)

	with col3:
		chart = CompanyCharts.get_rnd_selling(company)
		st.plotly_chart(chart, use_container_width=True)

	with col4:
		chart = CompanyCharts.get_simple_financials(company)
		st.plotly_chart(chart, use_container_width=True)

	with col5:
		chart = CompanyCharts.get_revenue_estimates(company)
		st.plotly_chart(chart, use_container_width=True)

	chart = CompanyCharts.get_key_metrics(company)
	st.plotly_chart(chart, use_container_width=True)