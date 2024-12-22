import fmpsdk  # type: ignore
import pandas as pd

from analysis.api.base_api import BaseAPI


class CompanyAPI(BaseAPI):
    @staticmethod
    async def get_company_profile(symbol: str) -> dict:
        url = f"/v3/profile/{symbol}"
        profile = await BaseAPI._get_async(url, {})
        return profile[0]

    @staticmethod
    async def get_daily_chart(symbol: str) -> pd.DataFrame:
        url = f"/v3/historical-price-full/{symbol}"
        daily_chart = await BaseAPI._get_async(url, {})
        return pd.DataFrame(daily_chart["historical"])

    @staticmethod
    async def get_daily_shares(symbol: str) -> pd.DataFrame:
        url = "/v4/historical/shares_float"
        params = {"symbol": symbol}
        daily_shares = await BaseAPI._get_async(url, params)
        return pd.DataFrame(daily_shares)

    @staticmethod
    async def get_full_quote(symbol: str) -> dict:
        url = f"/v3/quote/{symbol}"
        quote = await BaseAPI._get_async(url, {})
        return quote[0]

    @staticmethod
    async def get_bulk_prices(symbols: list[str]) -> list[dict]:
        url = "/v3/quote/" + ",".join(symbols)
        return await BaseAPI._get_async(url, {})

    @staticmethod
    def get_peers(symbol: str) -> list[str]:
        url = "/v4/stock_peers"
        params = {"symbol": symbol}
        return BaseAPI._get_request(url, params)[0]["peersList"]

    @staticmethod
    def get_employee_history(symbol: str) -> pd.DataFrame:
        url = "/v4/historical/employee_count"
        params = {"symbol": symbol}
        employees = BaseAPI._get_request(url, params)
        return pd.DataFrame.from_dict(employees)

    @staticmethod
    def get_executive_pay(symbol: str) -> pd.DataFrame:
        url = "/v4/governance/executive_compensation"
        params = {"symbol": symbol}
        executive_pay = BaseAPI._get_request(url, params)
        return pd.DataFrame.from_dict(executive_pay)

    @staticmethod
    async def get_balance_sheet_statements(
        symbol: str, period: str = "quarter"
    ) -> pd.DataFrame:
        url = f"/v3/balance-sheet-statement/{symbol}"
        params = {"period": period}
        balance_sheet_statements = await BaseAPI._get_async(url, params)
        return pd.DataFrame(balance_sheet_statements)

    @staticmethod
    async def get_income_statements(
        symbol: str, period: str = "quarter"
    ) -> pd.DataFrame:
        url = f"/v3/income-statement/{symbol}"
        params = {"period": period}
        income_statements = await BaseAPI._get_async(url, params)
        return pd.DataFrame(income_statements)

    @staticmethod
    async def get_cash_flow_statements(
        symbol: str, period: str = "quarter"
    ) -> pd.DataFrame:
        url = f"/v3/cash-flow-statement/{symbol}"
        params = {"period": period}
        cash_flow_statements = await BaseAPI._get_async(url, params)
        return pd.DataFrame(cash_flow_statements)

    @staticmethod
    async def get_ratios(symbol: str, period: str = "quarter") -> pd.DataFrame:
        url = f"/v3/ratios/{symbol}"
        params = {"period": period}
        ratios = await BaseAPI._get_async(url, params)
        return pd.DataFrame(ratios)

    @staticmethod
    async def get_key_metrics(symbol: str) -> pd.DataFrame:
        key_metrics = fmpsdk.key_metrics(
            apikey=BaseAPI._get_api_key(), symbol=symbol, period="quarter"
        )
        return pd.DataFrame(key_metrics)

    @staticmethod
    def get_news(symbol: str) -> pd.DataFrame:
        response = fmpsdk.stock_news(apikey=BaseAPI._get_api_key(), tickers=symbol)
        return pd.DataFrame(response)

    @staticmethod
    def get_insider_trades(symbol: str) -> pd.DataFrame:
        url = "/v4/insider-trading"
        params = {"symbol": symbol, "transactionType": "S-Sale"}
        response = BaseAPI._get_request(url, params)
        return pd.DataFrame.from_dict(response)

    @staticmethod
    async def get_analyst_estimates(symbol: str) -> pd.DataFrame:
        url = f"/v3/analyst-estimates/{symbol}"
        params = {"period": "quarter"}
        ratios = await BaseAPI._get_async(url, params)
        return pd.DataFrame(ratios)
