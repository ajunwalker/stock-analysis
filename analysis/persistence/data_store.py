import os
from datetime import datetime

from pymongo import MongoClient
from pymongo.synchronous.database import Database


class DataStore:
    db: Database

    _WATCHLIST = "watchlist"
    _HOLDINGS = "holdings"

    def __init__(self) -> None:
        client: MongoClient = MongoClient(os.environ["MONGO_URI"])
        self.db = client.get_database(os.environ["MONGO_DB_NAME"])

    def save_to_watchlist(self, symbol: str) -> None:
        """
        Saves a single ticker symbol to the watchlist.
        """
        document = {"symbol": symbol}
        self.db[self._WATCHLIST].insert_one(document)

    def remove_from_watchlist(self, symbol: str) -> None:
        """
        Removes a single ticker symbol from the watchlist.
        """
        document = {"symbol": symbol}
        self.db[self._WATCHLIST].delete_one(document)

    def get_watchlist(self) -> list[str]:
        """
        Returns a list of ticker symbols saved in the watchlist.
        """
        return [doc["symbol"] for doc in self.db[self._WATCHLIST].find()]

    def save_to_holdings(self, symbol: str) -> None:
        """
        Saves a single ticker symbol to the holding's collection.
        """
        document = {"symbol": symbol}
        self.db[self._HOLDINGS].insert_one(document)

    def remove_from_holdings(self, symbol: str) -> None:
        """
        Removes a single ticker symbol from the holding's collection.
        """
        document = {"symbol": symbol}
        self.db[self._HOLDINGS].delete_one(document)

    def get_holdings(self) -> list[str]:
        """
        Returns a list of ticker symbols saved in the holding's collection.
        """
        return [doc["symbol"] for doc in self.db[self._HOLDINGS].find()]

    @staticmethod
    def get_date() -> str:
        """
        Returns today's date in YYYY-MM-DD format.
        """
        return datetime.today().strftime("%Y-%m-%d")
