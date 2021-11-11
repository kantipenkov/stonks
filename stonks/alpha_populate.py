from enum import Enum
import json
from pathlib import Path
import requests
from pprint import pprint
import pdb
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()
from finansials.models import Company, CompanyIncomeStatements, ReportType


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


class AlphaVantage():
    api_key = None

    # implement time tracked our only 5 calls a minute and 500 calls a day are available
    # when request received we should wait if we exeeded available amount of calls

    # def __init__(self, api_key):
    #     self.api_key = api_key

    @classmethod
    def compose_url(cls, function, ticker, api_key):
        return f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={api_key}"

    @classmethod
    def get_income(cls, ticker):        
        logger.info(f"getting income statements for {ticker}")
        return cls.get_fundamentals(API_FUNCTIONS.INCOME.value, ticker)

    @classmethod
    def get_balance(cls, ticker):
        logger.info(f"getting balances for {ticker}")
        return cls.get_fundamentals(API_FUNCTIONS.BALANCE.value, ticker)

    @classmethod
    def get_cash_flows(cls, ticker):
        logger.info(f"getting cash flows for {ticker}")
        return cls.get_fundamentals(API_FUNCTIONS.CASH_FLOW.value, ticker)

    @classmethod
    def get_earnings(cls, ticker):
        logger.info(f"getting earnings for {ticker}")
        return cls.get_fundamentals(API_FUNCTIONS.EARNINGS.value, ticker)

    @classmethod
    def get_overview(cls, ticker):
        logger.info(f"getting overview for {ticker}")
        return cls.get_fundamentals(API_FUNCTIONS.OVERVIEW.value, ticker)

    @classmethod
    def get_fundamentals(cls, function, ticker):
        logger.info(f"request data for {ticker}")
        if not cls.api_key:
            raise NoApiKey("please set api key before pulling data from api" )
        url = cls.compose_url(function, ticker, cls.api_key)
        r = requests.get(url)
        data = r.json()
        return data

    @classmethod
    def get_all_fundamentals(cls, ticker):
        logger.info(f"getting all fundamentals for {ticker}")
        obj = TickerData(ticker)
        obj.income = cls.get_income(ticker)
        obj.balances = cls.get_balance(ticker)
        obj.cash_flows = cls.get_cash_flows(ticker)
        obj.earnings = cls.get_earnings(ticker)
        obj.overview = cls.get_overview(ticker)
        return obj


class TickerData():
    ticker = None
    income = None
    balances = None
    cash_flows = None
    earnings = None
    overview = None

    def __init__(self, ticker:str):
        self.ticker = ticker.upper()

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
        
            
        if not Company.objects.filter(ticker=self.ticker).count():
            logger.info(f"Add company {self.ticker}")
            if not self.overview:
                self.overview = AlphaVantage.get_overview(self.ticker)
            company = Company(
                                ticker=ticker,
                                name=self.overview["Name"],
                                description=self.overview["Description"],
                                industry=self.overview["Sector"],
                                sector=self.overview["Industry"] 
                             )
            company.save()
        else:
            logger.info(f"overview for {self.ticker} already exists")
            company = Company.objects.filter(ticker=self.ticker).get()
        # get all reports for the company and check if we have a new one in current report
        last_earnings_report = CompanyIncomeStatements.objects.filter(company=company).order_by("-date_reported").first()
        logger.info(last_earnings_report)
        if not last_earnings_report:
            if not self.income:
                self.income = AlphaVantage.get_income(self.ticker)
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.income[report_type]:

                    earnings = CompanyIncomeStatements(
                        company=company,
                        date_reported=report["fiscalDateEnding"],
                        report_type=db_report_type,
                        gross_profit=int(report["grossProfit"]),
                        total_revenue=int(report["totalRevenue"]),
                        cost_of_revenue=int(report["costOfRevenue"]),
                        cost_of_goods_and_services_sold=int(report["costofGoodsAndServicesSold"]),
                        operating_income=int(report["operatingIncome"]),
                        selling_general_and_administrative=int(report["sellingGeneralAndAdministrative"]),
                        rnd=int(report["researchAndDevelopment"]),
                        operating_expences=int(report["operatingExpenses"]),
                        investment_income_net=int(report["investmentIncomeNet"]),
                        net_interest_income=int(report["netInterestIncome"]),
                        interest_income=int(report["interestIncome"]),
                        interest_expense=int(report["interestExpense"]),
                        non_interest_income=int(report["nonInterestIncome"]),
                        other_non_operating_income=int(report["otherNonOperatingIncome"]),
                        deprecation=int(report["depreciation"]),
                        deprecation_and_amortization=int(report["depreciationAndAmortization"]),
                        income_before_tax=int(report["incomeBeforeTax"]),
                        income_tax_expence=int(report["incomeTaxExpense"]),
                        interest_and_debt_expence=int(report["interestAndDebtExpense"]),
                        net_income_from_continuing_operations=int(report["netIncomeFromContinuingOperations"]),
                        comprehensive_incom_net_of_tax=int(report["comprehensiveIncomeNetOfTax"]),
                        ebit=int(report["ebit"]),
                        ebitda=int(report["ebitda"]),
                        net_income=int(report["netIncome"]),
                    )
                    earnings.save()

            
        


if __name__ == '__main__':
    api_key = "VLFPX8TAR2XREWC2"
    api = AlphaVantage.api_key = api_key
    # for ticker in ('NVDA', 'AMD'):
    ticker = 'NVDA'

    backup_path = Path("backup2.json")
    with backup_path.open('r') as fh:
        ticker_dict = json.load(fh)
    ticker_data = TickerData(ticker)
    ticker_data.from_dict(ticker_dict)
    # company = Company.objects.filter(ticker=ticker).get()
    # cd = CompanyData(company=company, date_reported="2021-01-31", report_type=ReportType.Quarterly)
    import pdb;pdb.set_trace()
    ticker_data.update_database()

    # obj = api.get_all_fundamentals(ticker)

