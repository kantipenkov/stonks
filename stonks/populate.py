# import FundamentalAnalysis as fa
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()

from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CompanyEarnings, WatchItem, WatchList
from urllib.request import urlopen
import json
import pandas as pd
from datetime import datetime
api_key = '72005c1aeca3cf3319bcc2dccecbc243'

url_template = r"https://financialmodelingprep.com/api/v{api_version}/{request}?{arguments}"
# url_template.format(request = "", api_key = "")
def get_jsonparsed_data(request, api_key, arguments={}, api_version=3):
    arguments['apikey']=api_key
    arguments_str = '&'.join(map(lambda x: '='.join(map(str, x)), arguments.items()))
    url = url_template.format(api_version=api_version, request=request, arguments=arguments_str)
    print(url)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def create_company_data(ticker):
    if not Company.objects.filter(ticker=ticker).count():
        print(f"add company {ticker}")
        company_data = get_jsonparsed_data(f"profile/{ticker}", api_key)[0]
        company = Company(ticker=ticker, name=company_data["companyName"], description=company_data["description"])
        company.save()
    else:
        company = Company.objects.filter(ticker=ticker).get()

    last_report = CompanyEarnings.objects.filter(company=company).order_by("-date_reported").first()
    update_needed = False
    if last_report:
        if (datetime.now().date() - last_report.date_reported).days > 90:
            update_needed = True
    else:
        update_needed = True
    if update_needed:
        print("check for earnings update")
        company_earnings_data = get_jsonparsed_data(f"income-statement/{ticker}", api_key, {"limit": 120})
        for report in company_earnings_data:
            if not last_report or (last_report and datetime.strptime(report['date'], "%Y-%m-%d").date() > last_report.date_reported):
                print(f"add earnings report from {report['date']}")
                earnings = CompanyEarnings(
                    company=company,
                    date_reported=report["date"],
                    revenue=report["revenue"],
                    operating_income=report["operatingIncome"],
                    net_income=report["netIncome"],
                    income_before_tax=report["incomeBeforeTax"],
                    gross_profit=report["grossProfit"],
                    eps=report["eps"],
                    eps_diluted=report["epsdiluted"],
                    ebitda=report["ebitda"],
                    cost_of_revenue=report["costOfRevenue"],
                    interest_expence=report["interestExpense"],
                    rnd_expences=report["researchAndDevelopmentExpenses"]
                )
                earnings.save()
        
        company_balance_data = get_jsonparsed_data(f"balance-sheet-statement/{ticker}", api_key, {"limit": 120})
        for report in company_balance_data:
            if not last_report or (last_report and datetime.strptime(report['date'], "%Y-%m-%d").date() > last_report.date_reported):
                print(f"add balance report from {report['date']}")
                balance = CompanyBalance(
                    company = company,
                    date_reported = report["date"],
                    account_payables = report["accountPayables"],
                    cash = report["cashAndCashEquivalents"],
                    cash_and_short_investments = report["cashAndShortTermInvestments"],
                    deferred_revenue = report["deferredRevenue"],
                    goodwill = report["goodwill"],
                    intangible_assets = report["intangibleAssets"],
                    long_term_investments = report["longTermInvestments"],
                    long_term_debt = report["longTermDebt"],
                    net_debt = report["netDebt"],
                    net_receivables = report["netReceivables"],
                    other_assets = report["otherAssets"],
                    other_current_assets = report["otherCurrentAssets"],
                    other_current_liabilities = report["otherCurrentLiabilities"],
                    other_liabilities = report["otherLiabilities"],
                    other_non_current_assets = report["otherNonCurrentAssets"],
                    other_non_current_liabilities = report["otherNonCurrentLiabilities"],
                    property_plant_equipment_net = report["propertyPlantEquipmentNet"],
                    retained_earnings = report["retainedEarnings"],
                    short_term_debt = report["shortTermDebt"],
                    short_term_investments = report["shortTermInvestments"],
                    tax_assets = report["taxAssets"],
                    total_assets = report["totalAssets"],
                    total_current_assets = report["totalCurrentAssets"],
                    total_current_liabilities = report["totalCurrentLiabilities"],
                    total_debt = report["totalDebt"],
                    total_investments = report["totalInvestments"],
                    total_liabilities = report["totalLiabilities"],
                    total_non_current_assets = report["totalNonCurrentAssets"],
                    total_non_current_liabilities = report["totalNonCurrentLiabilities"],
                    total_stockholders_equity = report["totalStockholdersEquity"],
                )
                balance.save()

        company_cash_flow_data = get_jsonparsed_data(f"cash-flow-statement/{ticker}", api_key, {"limit": 120})
        for report in company_cash_flow_data:
            if not last_report or (last_report and datetime.strptime(report['date'], "%Y-%m-%d").date() > last_report.date_reported):
                print(f"add cash flow report from {report['date']}")
                cash_flow = CompanyCashFlow(
                    company = company,
                    date_reported = report["date"],
                    accounts_payables = report["accountsPayables"],
                    accounts_receuvables = report["accountsReceivables"],
                    acquisitions_net = report["acquisitionsNet"],
                    capital_expenditure = report["capitalExpenditure"],
                    cash_at_beginning = report["cashAtBeginningOfPeriod"],
                    cash_at_end = report["cashAtEndOfPeriod"],
                    change_in_work_capital = report["changeInWorkingCapital"],
                    common_stock_issued = report["commonStockIssued"],
                    common_stock_repurchased = report["commonStockRepurchased"],
                    debt_repayment = report["debtRepayment"],
                    deferred_income_tax = report["deferredIncomeTax"],
                    deprecation_and_amortization = report["depreciationAndAmortization"],
                    dividend_paid = report["dividendsPaid"],
                    free_cash_flow = report["freeCashFlow"],
                    inventory = report["inventory"],
                    investments_in_property = report["investmentsInPropertyPlantAndEquipment"],
                    cash_provided_by_operations = report["netCashProvidedByOperatingActivities"],
                    cash_used_for_investment = report["netCashUsedForInvestingActivites"],
                    cash_by_financing = report["netCashUsedProvidedByFinancingActivities"],
                    change_in_cash = report["netChangeInCash"],
                    operation_cash_flow = report["operatingCashFlow"],
                    other_financing_activities = report["otherFinancingActivites"],
                    other_investing_activities = report["otherInvestingActivites"],
                    other_non_cash_items = report["otherNonCashItems"],
                    other_working_capital = report["otherWorkingCapital"],
                    purchase_of_investments = report["purchasesOfInvestments"],
                    sales_maturity_of_investments = report["salesMaturitiesOfInvestments"],
                    stock_based_compensation = report["stockBasedCompensation"],
                )
                cash_flow.save()



def populate_fundamentals():
    tickers = ['NVDA', 'AMD', 'INTC']
    for ticker in tickers:
        create_company_data(ticker)

def populate_watchlists():
    wl_arr = WatchList.objects.all()
    wl_arr[0]
    company = Company.objects.filter(ticker='NVDA').get()
    watch_item = WatchItem(company=company, watch_list=wl_arr[0])
    watch_item.save()

    for company in Company.objects.all():
        watch_item = WatchItem(company=company, watch_list=wl_arr[1])
        watch_item.save()

import pdb;pdb.set_trace()


# fa.com

