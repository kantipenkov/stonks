# import FundamentalAnalysis as fa
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stonks.settings')
import django
django.setup()

from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CopmanyEarnings
from urllib.request import urlopen
import json
import pandas as pd
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
    company_data = get_jsonparsed_data(f"profile/{ticker}", api_key)[0]
    company = Company(ticker=ticker, name=company_data["companyName"], description=company_data["description"])
    company.save()

    company_earnings_data = get_jsonparsed_data(f"income-statement/{ticker}", api_key, {"limit": 120})
    for report in company_earnings_data:
        earnings = CopmanyEarnings(
            copmany=company,
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


ticker = 'AMD'


# fa.com
import pdb;pdb.set_trace()

