from django.db.models import fields
from rest_framework import serializers

# from django.contrib.auth.models import User
from finansials.models import Company, CompanyIncomeReport, CompanyBalanceReport
# from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CompanyEarnings, WatchList, WatchItem


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
    income_reports = serializers.HyperlinkedIdentityField(view_name="companyincomereport-detail")
    balance_reports = serializers.HyperlinkedIdentityField(view_name='companybalancereport-detail')
    # cash_flow = serializers.HyperlinkedIdentityField(view_name='company-cash-flow')


    class Meta:
        model = Company
        # fields = ['url', 'name', 'ticker', 'description', 'earnings', 'balance', 'cash_flow']
        fields = ['url', 'name', 'ticker', 'description', 'industry', 'sector', 'income_reports', 'balance_reports']

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
                  'operating_expences', 
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
                  'comprehensive_incom_net_of_tax',
                  'ebit',
                  'ebitda',
                  'net_income',
                 ]

class CompanyBalanceReportSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model =CompanyBalanceReport
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
                  'deffered_revenue',
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

# class CompanyCashFlowSerilaizer(serializers.HyperlinkedModelSerializer):
#     company = serializers.ReadOnlyField(source='company.name')

#     class Meta:
#         model = CompanyCashFlow
#         fields = [
#             'url',
#             'id',
#             'date_reported',
#             'accounts_payables',
#             'accounts_receuvables',
#             'acquisitions_net',
#             'capital_expenditure',
#             'cash_at_beginning',
#             'cash_at_end',
#             'change_in_work_capital',
#             'common_stock_issued',
#             'common_stock_repurchased',
#             'debt_repayment',
#             'deferred_income_tax',
#             'deprecation_and_amortization',
#             'dividend_paid',
#             'free_cash_flow',
#             'inventory',
#             'investments_in_property',
#             'cash_provided_by_operations',
#             'cash_used_for_investment',
#             'cash_by_financing',
#             'change_in_cash',
#             'operation_cash_flow',
#             'other_financing_activities',
#             'other_investing_activities',
#             'other_non_cash_items',
#             'other_working_capital',
#             'purchase_of_investments',
#             'sales_maturity_of_investments',
#             'stock_based_compensation',
#             'company',
#         ]


# class WatchListSerializer(serializers.HyperlinkedModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     # owner = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
#     watch_items = serializers.HyperlinkedIdentityField(view_name='watchlist-items')
    
#     class Meta:
#         model = WatchList
#         fields = ['url', 'id', 'name', 'owner', 'watch_items']
#         # fields = ['url', 'id', 'name', 'owner']


# class WatchItemSerializer(serializers.HyperlinkedModelSerializer):
#     company = UserSerializer
#     # company = serializers.ReadOnlyField(source='company.name')
#     watch_list = WatchListSerializer

#     class Meta:
#         model = WatchItem
#         fields = ['url', 'id', 'watch_list', 'company']
#         # fields = ['url', 'id', 'company']
