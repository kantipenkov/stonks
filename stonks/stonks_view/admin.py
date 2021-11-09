from django.contrib import admin
from stonks_view.models import Company, CompanyEarnings

# Register your models here.

admin.site.register(Company)
admin.site.register(CompanyEarnings)