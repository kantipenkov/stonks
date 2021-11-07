from enum import Enum
import json
from pathlib import Path
import requests
import pprint
import pdb


class API_FUNCTIONS(Enum):
    INCOME = "INCOME_STATEMENT"
    BALANCE = "BALANCE_SHEET"
    CASH_FLOW = "CASH_FLOW"
    EARNINGS = "EARNINGS"
    OVERVIEW = "OVERVIEW"

class NoDataException(Exception):
    "Please initialize object with get_all_fundamentals call"

class AlphaVantage:
    api_key = None
    income = None
    balances = None
    cash_flows = None
    earnings = None
    overview = None

    def __init__(self, api_key):
        self.api_key = api_key

    def compose_url(self, function, ticker, api_key):
        return f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={api_key}"

    def get_fundamentals(self, function, ticker):
        url = self.compose_url(function, ticker, api_key)
        r = requests.get(url)
        data = r.json()
        return data

    def get_income(self, ticker):
        self.income = self.get_fundamentals(API_FUNCTIONS.INCOME.value, ticker)
        return self.income

    def get_balance(self, ticker):
        self.balances = self.get_fundamentals(API_FUNCTIONS.BALANCE.value, ticker)
        return self.balances

    def get_cash_flows(self, ticker):
        self.cash_flows = self.get_fundamentals(API_FUNCTIONS.CASH_FLOW.value, ticker)
        return self.cash_flows

    def get_earnings(self, ticker):
        self.earnings = self.get_fundamentals(API_FUNCTIONS.EARNINGS.value, ticker)
        return self.earnings

    def get_everview(self, ticker):
        self.overview = self.get_fundamentals(API_FUNCTIONS.OVERVIEW.value, ticker)
        return self.overview

    def get_all_fundamentals(self, ticker):
        for func in (self.get_income, self.get_balance, self.get_cash_flows, self.get_earnings, self.get_everview):
            func(ticker)
        return self.to_json()
        
    def to_json(self):
        if not all((self.income, self.balances, self.cash_flows, self.earnings, self.overview)):
            raise NoDataException("Please initialize object with get_all_fundamentals call")
        data = {
            "income": self.income,
            "balances": self.balances,
            "cash_flows": self.cash_flows,
            "earnings": self.earnings,
            "overview": self.overview,
        }
        return data

    def save_to_file(self, path: Path):
        with backup_path.open('w') as fh:
            json.dump(api.to_json(), fh)

    def restore_from_file(self, path: Path):
        with backup_path.open('r') as fh:
            data = json.load(fh)
        self.income = data["income"]
        self.balances = data["balances"]
        self.cash_flows = data["cash_flows"]
        self.earnings = data["earnings"]
        self.overview = data["overview"]

if __name__ == '__main__':
    ticker = 'NVDA'
    api_key = "VLFPX8TAR2XREWC2"
    api = AlphaVantage(api_key)
    # api.income = "1"
    # api.balances = "12"
    # api.cash_flows = "13"
    # api.earnings = "14"
    # api.overview = "test"
    # api.get_all_fundamentals(ticker)
    backup_path = Path("backup.json")
    api.restore_from_file(backup_path)
    # api.save_to_file(backup_path)
    # income = api.get_income(ticker)
    pdb.set_trace()
    # print(income)
