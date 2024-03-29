from django.db.models import fields
from rest_framework import serializers

# from django.contrib.auth.models import User
from financials.models import Company, CompanyIncomeReport, CompanyBalanceReport, CompanyCashFlowReport, PricePoint


# class 

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

# class UserSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = User
#         fields = ['url', 'id', 'username']

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    income_annual_reports = serializers.HyperlinkedIdentityField(view_name="company-income-annual-reports")
    income_quarterly_reports = serializers.HyperlinkedIdentityField(view_name="company-income-quarterly-reports")
    balance_annual_reports = serializers.HyperlinkedIdentityField(view_name="company-balance-annual-reports")
    balance_quarterly_reports = serializers.HyperlinkedIdentityField(view_name="company-balance-quarterly-reports")
    cash_flow_annual_reports = serializers.HyperlinkedIdentityField(view_name="company-cash-flow-annual-reports")
    cash_flow_quarterly_reports = serializers.HyperlinkedIdentityField(view_name="company-cash-flow-quarterly-reports")
    price_history = serializers.HyperlinkedIdentityField(view_name='company-price-history')

    class Meta:
        model = Company
        fields = ['url',
                  'name',
                  'ticker',
                  'tinkoff_ticker',
                  'description',
                  'industry',
                  'sector',
                  'next_report_date',
                  'estimated_eps',
                  'currency',
                  'country',
                  'income_annual_reports',
                  'income_quarterly_reports',
                  'balance_annual_reports',
                  'balance_quarterly_reports',
                  'cash_flow_annual_reports',
                  'cash_flow_quarterly_reports',
                  'price_history',
                 ]

class CompanyIncomeReportSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = CompanyIncomeReport
        fields = ['url',
                  'id',
                  'company',
                  'date_reported',
                  'report_type',
                  'gross_profit', 
                  'total_revenue', 
                  'cost_of_revenue', 
                  'cost_of_goods_and_services_sold', 
                  'operating_income', 
                  'selling_general_and_administrative', 
                  'rnd', 
                  'operating_expenses', 
                  'investment_income_net', 
                  'net_interest_income', 
                  'interest_income',
                  'interest_expense',
                  'non_interest_income',
                  'other_non_operating_income',
                  'deprecation',
                  'deprecation_and_amortization',
                  'income_before_tax',
                  'income_tax_expence',
                  'interest_and_debt_expence',
                  'net_income_from_continuing_operations',
                  'comprehensive_income_net_of_tax',
                  'ebit',
                  'ebitda',
                  'net_income',
                 ]

class CompanyBalanceReportSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = CompanyBalanceReport
        fields = ['url',
                  'id',
                  'company',
                  'date_reported',
                  'report_type',
                  'total_assets',
                  'total_current_assets',
                  'cash_and_equivalents_at_carrying_value',
                  'cash_and_short_term_investments',
                  'inventory',
                  'current_net_receivables',
                  'total_non_current_assets',
                  'property_plant_equipment',
                  'accumulated_depreciation_amortization_ppe',
                  'intangible_assets',
                  'intangible_assets_excluding_goodwill',
                  'goodwill',
                  'investments',
                  'long_term_investments',
                  'short_term_investments',
                  'other_current_assets',
                  'other_non_current_assets',
                  'total_liabilities',
                  'total_current_liabilities',
                  'current_accounts_payable',
                  'deferred_revenue',
                  'current_debt',
                  'short_term_debt',
                  'total_non_current_liabilities',
                  'capital_lease_obligations',
                  'long_term_debt',
                  'current_long_term_debt',
                  'long_term_debt_non_current',
                  'short_long_term_debt_total',
                  'other_current_liabilities',
                  'other_non_current_liabilities',
                  'total_shareholder_equity',
                  'treasury_stock',
                  'retained_earnings',
                  'company_stock',
                  'common_stock_shares_outstanding',
                 ]

class CompanyCashFlowReportSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = CompanyCashFlowReport
        fields = ['url',
                  'id',
                  'company',
                  'date_reported',
                  'report_type',
                  'operating_cash_flow',
                  'payments_for_operating_activities',
                  'proceeds_from_operating_activities',
                  'change_in_operating_liabilities',
                  'change_in_operating_assets',
                  'depreciation_depletion_and_amortization',
                  'capital_expenditures',
                  'change_in_receivables',
                  'change_in_inventory',
                  'profit_loss',
                  'cash_flow_from_investment',
                  'cash_flow_from_financing',
                  'proceeds_from_repayment_of_short_term_debt',
                  'proceeds_for_repurchase_of_common_stock',
                  'proceeds_for_repurchase_of_equity',
                  'proceeds_for_repurchase_of_preferred_stock',
                  'dividend_payout',
                  'dividend_payout_common_stock',
                  'dividend_payout_preferred_stock',
                  'proceeds_from_issuance_of_common_stock',
                  'proceeds_from_issuance_of_long_term_debt_and_capital_securities',
                  'proceeds_from_issuance_of_preferred_stock',
                  'proceeds_from_repurchase_of_equity',
                  'proceeds_from_sale_of_treasury_stock',
                  'change_in_cash_and_cash_equivalents',
                  'change_in_exchange_rate',
                 ]


class PricePointSerializer(serializers.HyperlinkedModelSerializer):
  company = serializers.ReadOnlyField(source='company.name')
  class Meta:
    model = PricePoint
    fields = ['url',
              'id',
              'company',
              'date',
              'open',
              'high',
              'low',
              'close',
              'volume',
              'split_ratio',
             ]
