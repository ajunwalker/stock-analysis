from analysis.api.company_api import CompanyAPI
from analysis.api.market_api import MarketAPI
from analysis.api.screener_api import ScreenerAPI


class DataAPI(CompanyAPI, MarketAPI, ScreenerAPI):
	pass
