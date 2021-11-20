from django.contrib import admin
from finansials.models import Company, CompanyIncomeReport, CompanyBalanceReport

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyIncomeReport)
admin.site.register(CompanyBalanceReport)