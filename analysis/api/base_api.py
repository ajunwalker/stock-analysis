import os
from typing import Any

import httpx
import requests


class BaseAPI:
	_API_BASE_URL = "https://financialmodelingprep.com/api"

	@staticmethod
	def _get_request(url: str, params: Any) -> Any:
		params["apikey"] = BaseAPI._get_api_key()
		response = requests.get(url=BaseAPI._API_BASE_URL + url, params=params)
		return response.json()

	@staticmethod
	async def _get_async(url, params: Any) -> Any:
		params["apikey"] = BaseAPI._get_api_key()
		async with httpx.AsyncClient() as client:
			response = await client.get(BaseAPI._API_BASE_URL + url, params=params)
			return response.json()

	@staticmethod
	def _get_api_key() -> str:
		return os.environ["FMP_API_KEY"]
