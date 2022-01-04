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
    next_report_date = models.DateField(blank=True, default="2000-01-01")
    estimated_eps = models.FloatField(blank=True, default=0)




class CompanyIncomeReport(models.Model):
    company = models.ForeignKey(Company, related_name='income_reports', on_delete=models.CASCADE)
    date_reported = models.DateField()
    report_type = models.CharField(max_length=9, choices=ReportType.choices)
    gross_profit = models.BigIntegerField()
    total_revenue = models.BigIntegerField()
    cost_of_revenue = models.BigIntegerField()
    cost_of_goods_and_services_sold = models.BigIntegerField()
    operating_income = models.BigIntegerField()
    selling_general_and_administrative = models.BigIntegerField()
    rnd = models.BigIntegerField()
    operating_expenses = models.BigIntegerField()
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
    comprehensive_income_net_of_tax = models.BigIntegerField()
    ebit = models.BigIntegerField()
    ebitda = models.BigIntegerField()
    net_income = models.BigIntegerField()

    class Meta:
        ordering = ['date_reported']


class CompanyBalanceReport(models.Model):
    company = models.ForeignKey(Company, related_name='balance_reports', on_delete=models.CASCADE)
    date_reported = models.DateField()
    report_type = models.CharField(max_length=9, choices=ReportType.choices)
    total_assets = models.BigIntegerField()
    total_current_assets = models.BigIntegerField()
    cash_and_equivalents_at_carrying_value = models.BigIntegerField()
    cash_and_short_term_investments = models.BigIntegerField()
    inventory = models.BigIntegerField()
    current_net_receivables = models.BigIntegerField()
    total_non_current_assets = models.BigIntegerField()
    property_plant_equipment = models.BigIntegerField()
    accumulated_depreciation_amortization_ppe = models.BigIntegerField()
    intangible_assets = models.BigIntegerField()
    intangible_assets_excluding_goodwill = models.BigIntegerField()
    goodwill = models.BigIntegerField()
    investments = models.BigIntegerField()
    long_term_investments = models.BigIntegerField()
    short_term_investments = models.BigIntegerField()
    other_current_assets = models.BigIntegerField()
    other_non_current_assets = models.BigIntegerField()
    total_liabilities = models.BigIntegerField()
    total_current_liabilities = models.BigIntegerField()
    current_accounts_payable = models.BigIntegerField()
    deferred_revenue = models.BigIntegerField()
    current_debt = models.BigIntegerField()
    short_term_debt = models.BigIntegerField()
    total_non_current_liabilities = models.BigIntegerField()
    capital_lease_obligations = models.BigIntegerField()
    long_term_debt = models.BigIntegerField()
    current_long_term_debt = models.BigIntegerField()
    long_term_debt_non_current = models.BigIntegerField()
    short_long_term_debt_total = models.BigIntegerField()
    other_current_liabilities = models.BigIntegerField()
    other_non_current_liabilities = models.BigIntegerField()
    total_shareholder_equity = models.BigIntegerField()
    treasury_stock = models.BigIntegerField()
    retained_earnings = models.BigIntegerField()
    company_stock = models.BigIntegerField()
    common_stock_shares_outstanding = models.BigIntegerField()

    class Meta:
        ordering = ['date_reported']

class CompanyCashFlowReport(models.Model):
    company = models.ForeignKey(Company, related_name="cash_flows_reports", on_delete=models.CASCADE)
    date_reported = models.DateField()
    report_type = models.CharField(max_length=9, choices=ReportType.choices)
    operating_cash_flow = models.BigIntegerField()
    payments_for_operating_activities = models.BigIntegerField()
    proceeds_from_operating_activities = models.BigIntegerField()
    change_in_operating_liabilities = models.BigIntegerField()
    change_in_operating_assets = models.BigIntegerField()
    depreciation_depletion_and_amortization = models.BigIntegerField()
    capital_expenditures = models.BigIntegerField()
    change_in_receivables = models.BigIntegerField()
    change_in_inventory = models.BigIntegerField()
    profit_loss = models.BigIntegerField()
    cash_flow_from_investment = models.BigIntegerField()
    cash_flow_from_financing = models.BigIntegerField()
    proceeds_from_repayment_of_short_term_debt = models.BigIntegerField()
    proceeds_for_repurchase_of_common_stock = models.BigIntegerField()
    proceeds_for_repurchase_of_equity = models.BigIntegerField()
    proceeds_for_repurchase_of_preferred_stock = models.BigIntegerField()
    dividend_payout = models.BigIntegerField()
    dividend_payout_common_stock = models.BigIntegerField()
    dividend_payout_preferred_stock = models.BigIntegerField()
    proceeds_from_issuance_of_common_stock = models.BigIntegerField()
    proceeds_from_issuance_of_long_term_debt_and_capital_securities = models.BigIntegerField()
    proceeds_from_issuance_of_preferred_stock = models.BigIntegerField()
    proceeds_from_repurchase_of_equity = models.BigIntegerField()
    proceeds_from_sale_of_treasury_stock = models.BigIntegerField()
    change_in_cash_and_cash_equivalents = models.BigIntegerField()
    change_in_exchange_rate = models.BigIntegerField()

    class Meta:
        ordering = ['date_reported']

class PricePoint(models.Model):
    company = models.ForeignKey(Company, related_name="price_points", on_delete=models.CASCADE)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    split_ratio = models.DecimalField(max_digits=5, decimal_places=3, blank=True)

    class Meta:
        ordering = ['date']

