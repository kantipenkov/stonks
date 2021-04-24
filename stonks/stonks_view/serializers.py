from rest_framework import serializers

from django.contrib.auth.models import User
from stonks_view.models import Company, CompanyBalance, CompanyCashFlow, CopmanyEarnings


# class 

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username']

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    earnings = serializers.HyperlinkedIdentityField(view_name="company-earnings")
    
    class Meta:
        model = Company
        fields = ['url', 'name', 'ticker', 'description', 'earnings']

class CopmanyEarningsSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.ReadOnlyField(source='company.name')
    class Meta:
        model = CopmanyEarnings
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
