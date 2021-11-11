from django.db import models

# from django.contrib.auth.models import User

# Create your models here.

class ReportType(models.TextChoices):
    Annual = 'Annual'
    Quarterly = 'Quarterly'

class Company(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)




class CompanyIncomeStatements(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_reported = models.DateField()
    report_type = models.CharField(max_length=9, choices=ReportType.choices)
    gross_profit = models.BigIntegerField()
    total_revenue = models.BigIntegerField()
    cost_of_revenue = models.BigIntegerField()
    cost_of_goods_and_services_sold = models.BigIntegerField()
    operating_income = models.BigIntegerField()
    selling_general_and_administrative = models.BigIntegerField()
    rnd = models.BigIntegerField()
    operating_expences = models.BigIntegerField()
    investment_income_net = models.BigIntegerField()
    net_interest_income = models.BigIntegerField()
    interest_income = models.BigIntegerField()
    interest_expense = models.BigIntegerField()
    non_interest_income = models.BigIntegerField()
    other_non_operating_income = models.BigIntegerField()
    deprecation = models.BigIntegerField()
    deprecation_and_amortization = models.BigIntegerField()
    income_before_tax = models.BigIntegerField()
    income_tax_expence = models.BigIntegerField()
    interest_and_debt_expence = models.BigIntegerField()
    net_income_from_continuing_operations = models.BigIntegerField()
    comprehensive_incom_net_of_tax = models.BigIntegerField()
    ebit = models.BigIntegerField()
    ebitda = models.BigIntegerField()
    net_income = models.BigIntegerField()

    class Meta:
        ordering = ['date_reported']

# class CompanyBalance(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     date_reported = models.DateField()

#     account_payables = models.IntegerField()
#     cash = models.IntegerField()
#     cash_and_short_investments = models.IntegerField()
#     deferred_revenue = models.IntegerField()
#     goodwill = models.IntegerField()
#     intangible_assets = models.IntegerField()
#     long_term_investments = models.IntegerField()
#     long_term_debt = models.IntegerField()
#     net_debt = models.IntegerField()
#     net_receivables = models.IntegerField()
#     other_assets = models.IntegerField()
#     other_current_assets = models.IntegerField()
#     other_current_liabilities = models.IntegerField()
#     other_liabilities = models.IntegerField()
#     other_non_current_assets = models.IntegerField()
#     other_non_current_liabilities = models.IntegerField()
#     property_plant_equipment_net = models.IntegerField()
#     retained_earnings = models.IntegerField()
#     short_term_debt = models.IntegerField()
#     short_term_investments = models.IntegerField()
#     tax_assets = models.IntegerField()
#     total_assets = models.IntegerField()
#     total_current_assets = models.IntegerField()
#     total_current_liabilities = models.IntegerField()
#     total_debt = models.IntegerField()
#     total_investments = models.IntegerField()
#     total_liabilities = models.IntegerField()
#     total_non_current_assets = models.IntegerField()
#     total_non_current_liabilities = models.IntegerField()
#     total_stockholders_equity = models.IntegerField()


# class CompanyCashFlow(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     date_reported = models.DateField()

#     accounts_payables = models.IntegerField()
#     accounts_receuvables = models.IntegerField()
#     acquisitions_net = models.IntegerField()
#     capital_expenditure = models.IntegerField()
#     cash_at_beginning = models.IntegerField()
#     cash_at_end = models.IntegerField()
#     change_in_work_capital = models.IntegerField()
#     common_stock_issued = models.IntegerField()
#     common_stock_repurchased = models.IntegerField()
#     debt_repayment = models.IntegerField()
#     deferred_income_tax = models.IntegerField()
#     deprecation_and_amortization = models.IntegerField()
#     dividend_paid = models.IntegerField()
#     free_cash_flow = models.IntegerField()
#     inventory = models.IntegerField()
#     investments_in_property = models.IntegerField()
#     cash_provided_by_operations = models.IntegerField()
#     cash_used_for_investment = models.IntegerField()
#     cash_by_financing = models.IntegerField()
#     change_in_cash = models.IntegerField()
#     operation_cash_flow = models.IntegerField()
#     other_financing_activities = models.IntegerField()
#     other_investing_activities = models.IntegerField()
#     other_non_cash_items = models.IntegerField()
#     other_working_capital = models.IntegerField()
#     purchase_of_investments = models.IntegerField()
#     sales_maturity_of_investments = models.IntegerField()
#     stock_based_compensation = models.IntegerField()
