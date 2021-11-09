from enum import Enum
import json
from pathlib import Path
import requests
from pprint import pprint
import pdb

import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()
from stonks_view.models import Company, CompanyEarnings


class API_FUNCTIONS(Enum):
    INCOME = "INCOME_STATEMENT"
    BALANCE = "BALANCE_SHEET"
    CASH_FLOW = "CASH_FLOW"
    EARNINGS = "EARNINGS"
    OVERVIEW = "OVERVIEW"

class NoDataException(Exception):
    "Please initialize object with get_all_fundamentals call"
class NoApiKey(Exception):
    "Please set api key to pull some data from api"

class TickerData():
    ticker = None
    income = None
    balances = None
    cash_flows = None
    earnings = None
    overview = None

    def __init__(self, ticker):
        self.ticker = ticker

    def to_dict(self):
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

    def from_dict(self, data):
            self.income = data["income"]
            self.balances = data["balances"]
            self.cash_flows = data["cash_flows"]
            self.earnings = data["earnings"]
            self.overview = data["overview"]

    def update_database(self):
        if not Company.objects.filter(ticker=self.ticker.upper()).count():
            print(f"Add company {self.ticker}")
            company = Company(
                                ticker=ticker,
                                name=self.overview["Name"],
                                description=self.overview["Description"],
                                industry=self.overview["Sector"],
                                sector=self.overview["Industry"] 
                             )
            company.save()
        


class AlphaVantage(TickerData):
    api_key = None

    def __init__(self, api_key):
        self.api_key = api_key

    def compose_url(self, function, ticker, api_key):
        return f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={api_key}"

    def get_income(self, ticker):
        return self.get_fundamentals(API_FUNCTIONS.INCOME.value, ticker)

    def get_balance(self, ticker):
        return self.get_fundamentals(API_FUNCTIONS.BALANCE.value, ticker)

    def get_cash_flows(self, ticker):
        return self.get_fundamentals(API_FUNCTIONS.CASH_FLOW.value, ticker)

    def get_earnings(self, ticker):
        return self.get_fundamentals(API_FUNCTIONS.EARNINGS.value, ticker)

    def get_everview(self, ticker):
        return self.get_fundamentals(API_FUNCTIONS.OVERVIEW.value, ticker)

    def get_fundamentals(self, function, ticker):
        if not self.api_key:
            raise NoApiKey("please set api key before pulling data from api" )
        url = self.compose_url(function, ticker, api_key)
        r = requests.get(url)
        data = r.json()
        return data

    def get_all_fundamentals(self, ticker):
        obj = TickerData(ticker)
        # for func in (obj.get_income, obj.get_balance, obj.get_cash_flows, obj.get_earnings, obj.get_everview):
        #     func()
        obj.income = self.get_income(ticker)
        obj.balances = self.get_balance(ticker)
        obj.cash_flows = self.get_cash_flows(ticker)
        obj.earnings = self.get_earnings(ticker)
        obj.overview = self.get_everview(ticker)
        return obj

class AlphaVantageCollection(dict):
    api_key = None

    def to_dict(self):
        data = {}
        for key in self.keys():
            data[key] = self[key].to_dict()
        return data




if __name__ == '__main__':
    ticker = 'NVDA'
    api_key = "VLFPX8TAR2XREWC2"
    coll = AlphaVantageCollection()
    api = AlphaVantage(api_key)
    # obj = api.get_all_fundamentals(ticker)

    backup_path = Path("backup2.json")
    # # ticker_data = api.get_all_fundamentals(ticker)
    # ticker_data = TickerData(ticker)
    with backup_path.open('r') as fh:
        ticker_dict = json.load(fh)
    ticker_data = TickerData(ticker)
    ticker_data.from_dict(ticker_dict)
    import pdb;pdb.set_trace()

    # coll[ticker] = ticker_data
    # with backup_path.open('w') as fh:
    #     json.dump(coll.to_dict(), fh, indent=4)
