from django.db import models

# Create your models here.

class Company(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()



class CopmanyEarnings(models.Model):
    copmany = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_reported = models.DateField()

    revenue = models.IntegerField()
    operating_income = models.IntegerField()
    net_income = models.IntegerField()
    income_before_tax = models.IntegerField()
    gross_profit = models.IntegerField()
    eps = models.FloatField()
    eps_diluted = models.FloatField()
    ebitda = models.IntegerField()

    cost_of_revenue = models.IntegerField()
    interest_expence = models.IntegerField()
    rnd_expences = models.IntegerField()

class CompanyBalance(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_reported = models.DateField()

    account_payables = models.IntegerField()
    cash = models.IntegerField()
    cash_and_short_investments = models.IntegerField()
    deferred_revenue = models.IntegerField()
    goodwill = models.IntegerField()
    intangible_assets = models.IntegerField()
    long_term_investments = models.IntegerField()
    long_term_debt = models.IntegerField()
    net_debt = models.IntegerField()
    net_receivables = models.IntegerField()
    other_assets = models.IntegerField()
    other_current_assets = models.IntegerField()
    other_current_liabilities = models.IntegerField()
    other_liabilities = models.IntegerField()
    other_non_current_assets = models.IntegerField()
    other_non_current_liabilities = models.IntegerField()
    property_plant_equipment_net = models.IntegerField()
    retained_earnings = models.IntegerField()
    short_term_debt = models.IntegerField()
    short_term_investments = models.IntegerField()
    tax_assets = models.IntegerField()
    total_assets = models.IntegerField()
    total_current_assets = models.IntegerField()
    total_current_liabilities = models.IntegerField()
    total_debt = models.IntegerField()
    total_investments = models.IntegerField()
    total_liabilities = models.IntegerField()
    total_non_current_assets = models.IntegerField()
    total_non_current_liabilities = models.IntegerField()
    total_stockholders_equity = models.IntegerField()


class CompanyCashFlow(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_reported = models.DateField()

    accounts_payables = models.IntegerField()
    accounts_receuvables = models.IntegerField()
    acquisitions_net = models.IntegerField()
    capital_expenditure = models.IntegerField()
    cash_at_beginning = models.IntegerField()
    cash_at_end = models.IntegerField()
    change_in_work_capital = models.IntegerField()
    common_stock_issued = models.IntegerField()
    common_stock_repurchased = models.IntegerField()
    debt_repayment = models.IntegerField()
    deferred_income_tax = models.IntegerField()
    deprication_and_amortization = models.IntegerField()
    dividend_paid = models.IntegerField()
    free_cash_flow = models.IntegerField()
    inventory = models.IntegerField()
    investments_in_property = models.IntegerField()
    cash_provided_by_operations = models.IntegerField()
    cash_used_for_investment = models.IntegerField()
    cash_by_financing = models.IntegerField()
    change_in_cash = models.IntegerField()
    operation_cash_flow = models.IntegerField()
    other_financing_activities = models.IntegerField()
    other_investing_activities = models.IntegerField()
    other_non_cash_items = models.IntegerField()
    other_working_capital = models.IntegerField()
    purchase_of_investments = models.IntegerField()
    sales_maturity_of_investments = models.IntegerField()
    stock_based_compensation = models.IntegerField()

# class FinancialsDataModel(models.Model):
#     company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
#     origin = models.CharField(max_length=30)
#     date = models.DateField()
#     stockholders_equity = models.IntegerField()
#     total_assets = models.IntegerField()
#     current_assets = models.IntegerField()
#     total_liabilities = models.IntegerField()
#     current_liabilities = models.IntegerField()
#     net_income = models.IntegerField()
#     revenue = models.IntegerField()
#     operating_income = models.IntegerField()
#     net_margin = models.FloatField()
#     interest_expence = models.IntegerField()
#     operating_cash_flow = models.IntegerField()
#     shares_outstanding = models.IntegerField()
#     div_payout_ratio = models.FloatField()
#     interest_coverage = models.FloatField()
#     current_ratio = models.FloatField()
#     forward_eps = models.FloatField()
#     forward_pe = models.FloatField()
    

# class CurrentDataModel(models.Model):
#     company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
#     origin = models.CharField(max_length=30)
#     market_cap = models.FloatField()
#     current_price = models.FloatField()
#     pe = models.FloatField()
#     pb = models.FloatField()
#     ps = models.FloatField()
#     eps = models.FloatField()
#     div_yield = models.FloatField()
#     roe = models.FloatField()
#     roa = models.FloatField()
#     short_interest = models.FloatField()
#     beta = models.FloatField()

# class WatchListModel(models.Model): # reorganize to manytomany
#     name = models.CharField()
#     owner = models.ForeignKey(ProfileModel)

# class WatchListEntriesModel(models.Model):
#     company = models.ForeignKey(CompanyModel)
#     watch_list = models.ForeignKey(WatchListModel)

# class DesiredPriceModel(models.Model):
#     company = models.ForeignKey(CompanyModel, on_delete=models.DO_NOTHING)
#     desired_price = models.FloatField()
#     desired_pe = models.FloatField()
