from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()



class CompanyEarnings(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
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

    class Meta:
        ordering = ['date_reported']

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
    deprecation_and_amortization = models.IntegerField()
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


class WatchList(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class WatchItem(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    watch_list = models.ForeignKey(WatchList, on_delete=models.CASCADE)