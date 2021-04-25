from rest_framework import serializers

from django.contrib.auth.models import User
from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CompanyEarnings, WatchList, WatchItem


# class 

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    earnings = serializers.HyperlinkedIdentityField(view_name="company-earnings")
    balance = serializers.HyperlinkedIdentityField(view_name='company-balance')
    cash_flow = serializers.HyperlinkedIdentityField(view_name='company-cash-flow')


    class Meta:
        model = Company
        fields = ['url', 'name', 'ticker', 'description', 'earnings', 'balance', 'cash_flow']

class CompanyEarningsSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = CompanyEarnings
        fields = ['url',
                  'id',
                  'date_reported',
                  'revenue',
                  'operating_income', 
                  'net_income', 
                  'income_before_tax', 
                  'gross_profit', 
                  'eps', 
                  'eps_diluted', 
                  'ebitda', 
                  'cost_of_revenue', 
                  'interest_expence', 
                  'rnd_expences', 
                  'company',
                 ]

class CompanyBalanceSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = CompanyBalance
        fields = [
            'url',
            'id',
            'date_reported',
            'account_payables',
            'cash',
            'cash_and_short_investments',
            'deferred_revenue',
            'goodwill',
            'intangible_assets',
            'long_term_investments',
            'long_term_debt',
            'net_debt',
            'net_receivables',
            'other_assets',
            'other_current_assets',
            'other_current_liabilities',
            'other_liabilities',
            'other_non_current_assets',
            'other_non_current_liabilities',
            'property_plant_equipment_net',
            'retained_earnings',
            'short_term_debt',
            'short_term_investments',
            'tax_assets',
            'total_assets',
            'total_current_assets',
            'total_current_liabilities',
            'total_debt',
            'total_investments',
            'total_liabilities',
            'total_non_current_assets',
            'total_non_current_liabilities',
            'total_stockholders_equity',
            'company',
        ]

class CompanyCashFlowSerilaizer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = CompanyCashFlow
        fields = [
            'url',
            'id',
            'date_reported',
            'accounts_payables',
            'accounts_receuvables',
            'acquisitions_net',
            'capital_expenditure',
            'cash_at_beginning',
            'cash_at_end',
            'change_in_work_capital',
            'common_stock_issued',
            'common_stock_repurchased',
            'debt_repayment',
            'deferred_income_tax',
            'deprecation_and_amortization',
            'dividend_paid',
            'free_cash_flow',
            'inventory',
            'investments_in_property',
            'cash_provided_by_operations',
            'cash_used_for_investment',
            'cash_by_financing',
            'change_in_cash',
            'operation_cash_flow',
            'other_financing_activities',
            'other_investing_activities',
            'other_non_cash_items',
            'other_working_capital',
            'purchase_of_investments',
            'sales_maturity_of_investments',
            'stock_based_compensation',
            'company',
        ]


class WatchItemSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    watch_list = serializers.ReadOnlyField(source='watch_list.name')

    class Meta:
        model = WatchItem
        fields = ['url', 'id', 'watch_list', 'company']
        # fields = ['url', 'id', 'company']

class WatchListSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    watch_items = serializers.HyperlinkedIdentityField(view_name='watchlist-items')
    
    class Meta:
        model = WatchList
        fields = ['url', 'id', 'name', 'owner', 'watch_items']
        # fields = ['url', 'id', 'name', 'owner']
