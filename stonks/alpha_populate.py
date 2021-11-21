from pprint import pprint
import pdb

from datetime import datetime
from enum import Enum
import json
from pathlib import Path
import requests
import time

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
from finansials.models import Company, CompanyIncomeReport, ReportType, CompanyBalanceReport, CompanyCashFlowReport


def convert(val: str):
    try:
        return int(val)
    except ValueError:
        logger.debug(f"Improper value to convert ({val}). Return '0' instead")
        return 0

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


class ApiTimeoutManager():
    
    _max_requests_per_minute = 5
    _max_requests_per_day = 500
    _current_operrations_per_day = 0
    _current_operations_per_minute = 0
    _first_operation_timestamp = None
    _first_of_five_operations_timestamp = None

    @classmethod
    def set_requests_limiters(cls, minute: int, day: int):
        cls._max_requests_per_minute = minute
        cls._max_requests_per_day = day

    @classmethod
    def reset_minute_counter(cls):
        cls._first_of_five_operations_timestamp = time.time()
        cls._current_operations_per_minute = 1

    @classmethod
    def reset_day_counter(cls):
        cls._current_operrations_per_day = 1
        cls._first_operation_timestamp = time.time()

    @classmethod
    def check_api_timeout(cls):
        if not cls._first_operation_timestamp:
            cls._first_operation_timestamp = time.time()
            cls._first_of_five_operations_timestamp = cls._first_operation_timestamp
        cls._current_operrations_per_day += 1
        cls._current_operations_per_minute += 1
        if cls._current_operations_per_minute > cls._max_requests_per_minute:
            diff = time.time() - cls._first_of_five_operations_timestamp
            minute_in_seconds = 60
            if diff < minute_in_seconds:
                break_time = minute_in_seconds - diff + 2 # to be sure
                logger.info(f"Exceed max amount of requests per minute wait for {break_time} seconds")
                time.sleep(break_time)
                cls.reset_minute_counter()
            else:
                cls.reset_minute_counter()
        
        if cls._current_operrations_per_day > cls._max_requests_per_day:
            diff =  time.time() - cls._first_operation_timestamp
            day_in_seconds = 24 * 60 * 60
            if diff < day_in_seconds:
                break_time = day_in_seconds - diff + 60 # just to be sure
                logger.info(f"Exceed maximum requests per day. Will wait for {time.strftime('%H hours %M minutes and %S seconds', time.gmtime(break_time))} seconds")
                time.sleep(break_time)
                cls.reset_day_counter
            else:
                cls.reset_day_counter()
                time.str


class AlphaVantage():
    api_key = None

    # implement time tracked our only 5 calls a minute and 500 calls a day are available
    # when request received we should wait if we exeeded available amount of calls

    @classmethod
    def check_api_timeout(cls):
        ApiTimeoutManager.check_api_timeout()

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
        cls.check_api_timeout()
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

    def _update_db_income(self, company):
        last_income_report = CompanyIncomeReport.objects.filter(company=company).order_by("-date_reported").first()
        
        existing_income_reports = list()
        update_required = False
        if last_income_report:
            cur_date = datetime.now().date()
            if (cur_date - last_income_report.date_reported).days > 90:
                update_required = True
                existing_income_reports = list(map(lambda x: (x[0].strftime("%Y-%m-%d"), x[1]), CompanyIncomeReport.objects.filter(company=company).values_list('date_reported', 'report_type')))

        else:
            update_required = True

        if update_required:
            logger.debug("checking for new income reports for {self.tcker}")
            if not self.income:
                self.income = AlphaVantage.get_income(self.ticker)
            # collect income statements
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.income[report_type]:
                    #check that there is no report from this date and the same report type
                    if not (report["fiscalDateEnding"], db_report_type) in existing_income_reports:
                        logger.info(f"New report income for ticker {self.ticker}. Date of report: {report['fiscalDateEnding']}, report type: {db_report_type}")
                        income_report = CompanyIncomeReport(
                            company=company,
                            date_reported=report["fiscalDateEnding"],
                            report_type=db_report_type,
                            gross_profit=convert(report["grossProfit"]),
                            total_revenue=convert(report["totalRevenue"]),
                            cost_of_revenue=convert(report["costOfRevenue"]),
                            cost_of_goods_and_services_sold=convert(report["costofGoodsAndServicesSold"]),
                            operating_income=convert(report["operatingIncome"]),
                            selling_general_and_administrative=convert(report["sellingGeneralAndAdministrative"]),
                            rnd=convert(report["researchAndDevelopment"]),
                            operating_expences=convert(report["operatingExpenses"]),
                            investment_income_net=convert(report["investmentIncomeNet"]),
                            net_interest_income=convert(report["netInterestIncome"]),
                            interest_income=convert(report["interestIncome"]),
                            interest_expense=convert(report["interestExpense"]),
                            non_interest_income=convert(report["nonInterestIncome"]),
                            other_non_operating_income=convert(report["otherNonOperatingIncome"]),
                            deprecation=convert(report["depreciation"]),
                            deprecation_and_amortization=convert(report["depreciationAndAmortization"]),
                            income_before_tax=convert(report["incomeBeforeTax"]),
                            income_tax_expence=convert(report["incomeTaxExpense"]),
                            interest_and_debt_expence=convert(report["interestAndDebtExpense"]),
                            net_income_from_continuing_operations=convert(report["netIncomeFromContinuingOperations"]),
                            comprehensive_incom_net_of_tax=convert(report["comprehensiveIncomeNetOfTax"]),
                            ebit=convert(report["ebit"]),
                            ebitda=convert(report["ebitda"]),
                            net_income=convert(report["netIncome"]),
                        )
                        income_report.save()

    def _update_db_balance(self, company):
        last_balance_report = CompanyBalanceReport.objects.filter(company=company).order_by("-date_reported").first()
        
        existing_balance_reports = list()
        update_required = False
        if last_balance_report:
            cur_date = datetime.now().date()
            if (cur_date - last_balance_report.date_reported).days > 90:
                update_required = True
                existing_balance_reports = list(map(lambda x: (x[0].strftime("%Y-%m-%d"), x[1]), CompanyBalanceReport.objects.filter(company=company).values_list('date_reported', 'report_type')))
        else:
            update_required = True

        if update_required:
            logger.debug("checking for new balance reports for {self.tcker}")
            if not self.balances:
                self.balances = AlphaVantage.get_balance(self.ticker)
            # collect balance statements
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.balances[report_type]:
                    #check that there is no report from this date and the same report type
                    if not (report["fiscalDateEnding"], db_report_type) in existing_balance_reports:
                        logger.info(f"New report balance for ticker {self.ticker}. Date of report: {report['fiscalDateEnding']}, report type: {db_report_type}")
                        balance_report = CompanyBalanceReport(
                            
                            company = company,
                            date_reported = report["fiscalDateEnding"],
                            report_type = db_report_type,
                            total_assets = convert(report["totalAssets"]),
                            total_current_assets = convert(report["totalCurrentAssets"]),
                            cash_and_equivalents_at_carrying_value = convert(report["cashAndCashEquivalentsAtCarryingValue"]),
                            cash_and_short_term_investments = convert(report["cashAndShortTermInvestments"]),
                            inventory = convert(report["inventory"]),
                            current_net_receivables = convert(report["currentNetReceivables"]),
                            total_non_current_assets = convert(report["totalNonCurrentAssets"]),
                            property_plant_equipment = convert(report["propertyPlantEquipment"]),
                            accumulated_depreciation_amortization_ppe = convert(report["accumulatedDepreciationAmortizationPPE"]),
                            intangible_assets = convert(report["intangibleAssets"]),
                            intangible_assets_excluding_goodwill = convert(report["intangibleAssetsExcludingGoodwill"]),
                            goodwill = convert(report["goodwill"]),
                            investments = convert(report["investments"]),
                            long_term_investments = convert(report["longTermInvestments"]),
                            short_term_investments = convert(report["shortTermInvestments"]),
                            other_current_assets = convert(report["otherCurrentAssets"]),
                            other_non_current_assets = convert(report["otherNonCurrrentAssets"]),
                            total_liabilities = convert(report["totalLiabilities"]),
                            total_current_liabilities = convert(report["totalCurrentLiabilities"]),
                            current_accounts_payable = convert(report["currentAccountsPayable"]),
                            deffered_revenue = convert(report["deferredRevenue"]),
                            current_debt = convert(report["currentDebt"]),
                            short_term_debt = convert(report["shortTermDebt"]),
                            total_non_current_liabilities = convert(report["totalNonCurrentLiabilities"]),
                            capital_lease_obligations = convert(report["capitalLeaseObligations"]),
                            long_term_debt = convert(report["longTermDebt"]),
                            current_long_term_debt = convert(report["currentLongTermDebt"]),
                            long_term_debt_non_current = convert(report["longTermDebtNoncurrent"]),
                            short_long_term_debt_total = convert(report["shortLongTermDebtTotal"]),
                            other_current_liabilities = convert(report["otherCurrentLiabilities"]),
                            other_non_current_liabilities = convert(report["otherNonCurrentLiabilities"]),
                            total_shareholder_equity = convert(report["totalShareholderEquity"]),
                            treasury_stock = convert(report["treasuryStock"]),
                            retained_earnings = convert(report["retainedEarnings"]),
                            company_stock = convert(report["commonStock"]),
                            common_stock_shares_outstanding = convert(report["commonStockSharesOutstanding"]),
                        )
                        balance_report.save()

    def _update_db_cash_flows(self, company):
        last_cash_flow_report = CompanyCashFlowReport.objects.filter(company=company).order_by("-date_reported").first()
        
        existing_cash_flow_reports = list()
        update_required = True
        if last_cash_flow_report:
            cur_date = datetime.now().date()
            if (cur_date - last_cash_flow_report.date_reported).days > 90:
                update_required = True
                existing_cash_flow_reports = list(map(lambda x: (x[0].strftime("%Y-%m-%d"), x[1]), CompanyCashFlowReport.objects.filter(company=company).values_list('date_reported', 'report_type')))
        else:
            update_required = True
        if update_required:
            logger.debug("checking for new cash flow reports for {self.tcker}")
            if not self.cash_flows:
                self.cash_flows = AlphaVantage.get_cash_flows(self.ticker)
        # collect cash_flow statements
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.cash_flows[report_type]:
                    #check that there is no report from this date and the same report type
                    if not (report["fiscalDateEnding"], db_report_type) in existing_cash_flow_reports:
                        logger.info(f"New report cash flow for ticker {self.ticker}. Date of report: {report['fiscalDateEnding']}, report type: {db_report_type}")
                        cash_flow_report = CompanyCashFlowReport(
                            
                            company = company,
                            date_reported = report["fiscalDateEnding"],
                            report_type = db_report_type,
                            operating_cash_flow = convert(report["operatingCashflow"]),
                            payments_for_operating_activities = convert(report["paymentsForOperatingActivities"]),
                            proceeds_from_operating_activities = convert(report["proceedsFromOperatingActivities"]),
                            change_in_operating_liabilities = convert(report["changeInOperatingLiabilities"]),
                            change_in_operating_assets = convert(report["changeInOperatingAssets"]),
                            depreciation_depletion_and_amortization = convert(report["depreciationDepletionAndAmortization"]),
                            capital_expenditures = convert(report["capitalExpenditures"]),
                            change_in_receivables = convert(report["changeInReceivables"]),
                            change_in_inventory = convert(report["changeInInventory"]),
                            profit_loss = convert(report["profitLoss"]),
                            cash_flow_from_investment = convert(report["cashflowFromInvestment"]),
                            cash_flow_from_financing = convert(report["cashflowFromFinancing"]),
                            proceeds_from_repayment_of_short_term_debt = convert(report["proceedsFromRepaymentsOfShortTermDebt"]),
                            proceeds_for_repurchase_of_common_stock = convert(report["paymentsForRepurchaseOfCommonStock"]),
                            proceeds_for_repurchase_of_equity = convert(report["paymentsForRepurchaseOfEquity"]),
                            proceeds_for_repurchase_of_preferred_stock = convert(report["paymentsForRepurchaseOfPreferredStock"]),
                            divident_payout = convert(report["dividendPayout"]),
                            divident_payout_common_stock = convert(report["dividendPayoutCommonStock"]),
                            divident_payout_preferred_stock = convert(report["dividendPayoutPreferredStock"]),
                            proceeds_from_issuance_of_common_stock = convert(report["proceedsFromIssuanceOfCommonStock"]),
                            proceeds_from_issuance_of_long_term_debt_and_capital_securities = convert(report["proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet"]),
                            proceeds_from_issuance_of_preferred_stock = convert(report["proceedsFromIssuanceOfPreferredStock"]),
                            proceeds_from_repurchase_of_equity = convert(report["proceedsFromRepurchaseOfEquity"]),
                            proceeds_from_sale_of_treasury_stock = convert(report["proceedsFromSaleOfTreasuryStock"]),
                            change_in_cash_and_cash_equivalents = convert(report["changeInCashAndCashEquivalents"]),
                            change_in_exchange_rate = convert(report["changeInExchangeRate"]),
                        )
                        cash_flow_report.save()
        

    def update_database(self):
        
        def convert(val: str):
            try:
                return int(val)
            except ValueError:
                logger.debug(f"Improper value to convert ({val}). Return '0' instead")
                return 0

        if not Company.objects.filter(ticker=self.ticker).count():
            logger.info(f"Add company {self.ticker}")
            if not self.overview:
                self.overview = AlphaVantage.get_overview(self.ticker)
            company = Company(
                                ticker=self.ticker,
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
        self._update_db_income(company)
        self._update_db_balance(company)
        self._update_db_cash_flows(company)
        
def api_timeout_manager_test():
    ApiTimeoutManager.set_requests_limiters(5, 12)
    start_time = time.time()
    
    for i in range(1,15):
        logger.debug(f"attempt {i}, time from start {time.time() - start_time} seconds")
        ApiTimeoutManager.check_api_timeout()
        time.sleep(1)


if __name__ == '__main__':
    api_key = "VLFPX8TAR2XREWC2"
    api = AlphaVantage.api_key = api_key
    # for ticker in ('NVDA', 'AMD'):
    ticker = 'INTC'

    # backup_path = Path("backup2.json")
    # with backup_path.open('r') as fh:
    #     ticker_dict = json.load(fh)
    ticker_data = TickerData(ticker)
    # ticker_data.from_dict(ticker_dict)
    # company = Company.objects.filter(ticker=ticker).get()
    # cd = CompanyData(company=company, date_reported="2021-01-31", report_type=ReportType.Quarterly)
    import pdb;pdb.set_trace()
    ticker_data.update_database()

    # obj = api.get_all_fundamentals(ticker)

