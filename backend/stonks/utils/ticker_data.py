from pprint import pprint


from datetime import datetime
import numpy as np
from typing import Optional


import logging
logger = logging.getLogger('root')


from utils.alpha_vantage import AlphaVantage
from utils.price_time_series import process_prices, PricePointTuple
from financials.models import Company, CompanyIncomeReport, ReportType, CompanyBalanceReport, CompanyCashFlowReport, PricePoint


class NoDataException(Exception):
    """Please initialize object with get_all_fundamentals call"""


class NoTickerException(Exception):
    """Ticker field hasn't been initialized"""


class TickerNotFound(Exception):
    """Failed to get correct data from API"""


def convert(val: str):
    try:
        return int(val)
    except ValueError:
        logger.debug(f"Improper value to convert ({val}). Return '0' instead")
        return 0

def update_earnings_dates(foresight_period=6, ticker: Optional[str]=None):
    update_required = False
    now = datetime.now().date()
    if ticker:
        ticker = ticker.upper()
        company = Company.objects.filter(ticker=ticker).get()
        if now > company.next_report_date:
            update_required = True
    else:
        for company in Company.objects.all():
            if now > company.next_report_date:
                update_required = True
                break
    if update_required:
        data = AlphaVantage.get_earnings_calendar(foresight_period, ticker)
        upcoming_earnings = np.array(','.join(data.split('\r\n')).split(',')[:-1]).reshape(-1, 6)
        # cut of headings and unused data
        upcoming_earnings = upcoming_earnings[1:, (0, 2, 4)]
        if ticker:
            company = Company.objects.filter(ticker=ticker).get()
            dates = np.stack(np.vectorize(datetime.strptime)(upcoming_earnings[:, 1], "%Y-%m-%d"))
            dates = np.stack(np.vectorize(datetime.timestamp)(dates))
            earnings_date = upcoming_earnings[np.argmin(dates), 1]
            estimated_eps = upcoming_earnings[np.argmin(dates), 2]
            company.next_report_date = earnings_date
            if estimated_eps:
                logger.info(f"Set estimated EPS for {company.ticker} to {estimated_eps}")
                company.estimated_eps = float(estimated_eps)
            logger.info(f"Set new report date for {company.ticker} as {earnings_date}")
            company.save()

        else:
            for company in Company.objects.all():
                # get only records for current company
                earnings = upcoming_earnings[np.where(upcoming_earnings[:, :1] == company.ticker)[0], :]
                if len(earnings) > 0:
                    dates = np.stack(np.vectorize(datetime.strptime)(earnings[:, 1], "%Y-%m-%d"))
                    dates = np.stack(np.vectorize(datetime.timestamp)(dates))
                    earnings_date = earnings[np.argmin(dates), 1]
                    estimated_eps = earnings[np.argmin(dates), 2]
                    company.next_report_date = earnings_date
                    if estimated_eps:
                        logger.info(f"Set estimated EPS for {company.ticker} to {estimated_eps}")
                        company.estimated_eps = float(estimated_eps)
                    logger.info(f"Set new report date for {company.ticker} as {earnings_date}")
                    company.save()

def check_ticker(f):
    def wrapper(*args):
        if not args[0].ticker:
            raise NoTickerException(f"please initialize ticker filed of the class before calling {f.__name__}")
        return f(*args)
    return wrapper


class TickerData():
    ticker = None
    income = None
    balances = None
    cash_flows = None
    earnings = None
    overview = None
    price_series = None

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
            if (cur_date - last_income_report.date_reported).days > 365:
                update_required = True
                existing_income_reports = list(map(lambda x: (x[0].strftime("%Y-%m-%d"), x[1]), CompanyIncomeReport.objects.filter(company=company).values_list('date_reported', 'report_type')))

        else:
            update_required = True
        
        if update_required:
            logger.debug("checking for new income reports for {self.ticker}")
            if not self.income:
                self.income = AlphaVantage.get_income(self.ticker)
            # collect income statements
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.income[report_type]:
                    #check that there is no report from this date and the same report type
                    if not (report["fiscalDateEnding"], db_report_type) in existing_income_reports:
                        logger.debug(f"New report income for ticker {self.ticker}. Date of report: {report['fiscalDateEnding']}, report type: {db_report_type}")
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
                            operating_expenses=convert(report["operatingExpenses"]),
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
                            comprehensive_income_net_of_tax=convert(report["comprehensiveIncomeNetOfTax"]),
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
            if (cur_date - last_balance_report.date_reported).days > 365:
                update_required = True
                existing_balance_reports = list(map(lambda x: (x[0].strftime("%Y-%m-%d"), x[1]), CompanyBalanceReport.objects.filter(company=company).values_list('date_reported', 'report_type')))
        else:
            update_required = True

        if update_required:
            logger.debug("checking for new balance reports for {self.ticker}")
            if not self.balances:
                self.balances = AlphaVantage.get_balance(self.ticker)
            # collect balance statements
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.balances[report_type]:
                    #check that there is no report from this date and the same report type
                    if not (report["fiscalDateEnding"], db_report_type) in existing_balance_reports:
                        logger.debug(f"New report balance for ticker {self.ticker}. Date of report: {report['fiscalDateEnding']}, report type: {db_report_type}")
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
                            deferred_revenue = convert(report["deferredRevenue"]),
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
        update_required = False
        if last_cash_flow_report:
            cur_date = datetime.now().date()
            if (cur_date - last_cash_flow_report.date_reported).days > 365:
                update_required = True
                existing_cash_flow_reports = list(map(lambda x: (x[0].strftime("%Y-%m-%d"), x[1]), CompanyCashFlowReport.objects.filter(company=company).values_list('date_reported', 'report_type')))
        else:
            update_required = True

        if update_required:
            logger.debug(f"checking for new cash flow reports for {self.ticker}")
            if not self.cash_flows:
                self.cash_flows = AlphaVantage.get_cash_flows(self.ticker)
        # collect cash_flow statements
            for report_type, db_report_type in (("annualReports", ReportType.Annual), ("quarterlyReports", ReportType.Quarterly)):
                for report in self.cash_flows[report_type]:
                    #check that there is no report from this date and the same report type
                    if not (report["fiscalDateEnding"], db_report_type) in existing_cash_flow_reports:
                        logger.debug(f"New report cash flow for ticker {self.ticker}. Date of report: {report['fiscalDateEnding']}, report type: {db_report_type}")
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
                            dividend_payout = convert(report["dividendPayout"]),
                            dividend_payout_common_stock = convert(report["dividendPayoutCommonStock"]),
                            dividend_payout_preferred_stock = convert(report["dividendPayoutPreferredStock"]),
                            proceeds_from_issuance_of_common_stock = convert(report["proceedsFromIssuanceOfCommonStock"]),
                            proceeds_from_issuance_of_long_term_debt_and_capital_securities = convert(report["proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet"]),
                            proceeds_from_issuance_of_preferred_stock = convert(report["proceedsFromIssuanceOfPreferredStock"]),
                            proceeds_from_repurchase_of_equity = convert(report["proceedsFromRepurchaseOfEquity"]),
                            proceeds_from_sale_of_treasury_stock = convert(report["proceedsFromSaleOfTreasuryStock"]),
                            change_in_cash_and_cash_equivalents = convert(report["changeInCashAndCashEquivalents"]),
                            change_in_exchange_rate = convert(report["changeInExchangeRate"]),
                        )
                        cash_flow_report.save()

    def _update_time_series(self, company):
        update_required = False
        last_price_point = PricePoint.objects.filter(company=company).order_by('-date').first()
        if not last_price_point:
            update_required = True
        else:
            if (datetime.now().date() - last_price_point.date).days > 50:
                update_required = True
        if update_required:
            logger.info(f"Update prices history for {company.ticker}")
            existing_price_points = list(map(lambda x: datetime.combine(x[0], datetime.min.time()).timestamp(), PricePoint.objects.filter(company=company).values_list('date') ))
            # we should request only data we need not all the data
            price_series = AlphaVantage.get_price_series(self.ticker)
            price_series, splits = process_prices(price_series)
            # get existing values
            for elem in price_series:
                day_data = PricePointTuple(*elem)
                if day_data.timestamp not in existing_price_points:
                    kwargs = {
                        "company": company,
                        "date": day_data.date,
                        "open": float(day_data.open),
                        "high": float(day_data.high),
                        "low": float(day_data.low),
                        "close": float(day_data.close),
                        "volume": float(day_data.volume),
                    }
                    # splits processing should be moved to a separate operation
                    if day_data.timestamp in splits:
                        id = np.where(splits == day_data.timestamp)[0][0]
                        split = splits[id, 1]
                        kwargs["split_ratio"] = f"{split.numerator}:{split.denominator}"
                    logger.debug(f"Add Price point for {self.ticker} date: {day_data.date}")
                    price_point = PricePoint(**kwargs)
                    price_point.save()

    @check_ticker
    def update_db_fundamentals(self):
        if not Company.objects.filter(ticker=self.ticker).count():
            logger.info(f"Add company {self.ticker}")
            tinkoff_ticker = self.ticker
            if not self.overview:
                self.overview = AlphaVantage.get_overview(self.ticker)
                if not self.overview:
                    # use search node to find proper name of the ticker
                    search_results = AlphaVantage.search_tickers(self.ticker)
                    if len(search_results['bestMatches']) == 0:
                        raise TickerNotFound(f"failed to get data for {self.ticker} from API.")
                    if len(search_results['bestMatches']) > 1:
                        raise TickerNotFound(f"failed to get data for {self.ticker} from API. Search found to many results. Manual input required")
                    self.ticker = search_results['bestMatches'][0]['1. symbol']
                    self.overview = AlphaVantage.get_overview(self.ticker)
                    if not self.overview:
                        raise TickerNotFound(f"Cant fetch data for {self.ticker}")
                    
            # import pdb;pdb.set_trace()
            company = Company(
                                ticker=self.ticker,
                                tinkoff_ticker = tinkoff_ticker,
                                name=self.overview["Name"],
                                description=self.overview["Description"],
                                industry=self.overview["Sector"],
                                sector=self.overview["Industry"],
                                currency=self.overview["Currency"],
                                country=self.overview["Country"],
                             )
            company.save()
        else:
            logger.info(f"overview for {self.ticker} already exists")
            company = Company.objects.filter(ticker=self.ticker).get()
        # get all reports for the company and check if we have a new one in current report
        self._update_db_income(company)
        self._update_db_balance(company)
        self._update_db_cash_flows(company)
        self. _update_time_series(company)

    @check_ticker
    def get_all_fundamentals(self):
        logger.info(f"getting all fundamentals for {self.ticker}")
        self.income = AlphaVantage.get_income(self.ticker)
        self.balances = AlphaVantage.get_balance(self.ticker)
        self.cash_flows = AlphaVantage.get_cash_flows(self.ticker)
        self.earnings = AlphaVantage.get_earnings(self.ticker)
        self.overview = AlphaVantage.get_overview(self.ticker)
        self.price_series = AlphaVantage.get_price_series(self.ticker)
