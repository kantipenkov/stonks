from django.db import models

# Create your models here.

class CompanyModel(models.Model):
    name = models.CharField()
    ticker = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    last_earnings_update = models.DateField()
    last_metricks_update = models.DateTimeField()


class FinancialsDataModel(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.DO_NOTHING)
    origin = models.CharField()
    date = models.DateField()
    stockholders_equity = models.IntegerField()
    total_assets = models.IntegerField()
    current_assets = models.IntegerField()
    total_liabilities = models.IntegerField()
    current_liabilities = models.IntegerField()
    net_income = models.IntegerField()
    revenue = models.IntegerField()
    operating_income = models.IntegerField()
    net_margin = models.FloatField()
    interest_expence = models.IntegerField()
    operating_cash_flow = models.IntegerField()
    shares_outstanding = models.IntegerField()
    div_payout_ratio = models.FloatField()
    interest_coverage = models.FloatField()
    current_ratio = models.FloatField()
    forward_eps = models.FloatField()
    forward_pe = models.FloatField()
    

class CurrentDataModel(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.DO_NOTHING)
    origin = models.CharField()
    market_cap = models.FloatField()
    current_price = models.FloatField()
    pe = models.FloatField()
    pb = models.FloatField()
    ps = models.FloatField()
    eps = models.FloatField()
    div_yield = models.FloatField()
    roe = models.FloatField()
    roa = models.FloatField()
    short_interest = models.FloatField()
    beta = models.FloatField()

# class WatchListModel(models.Model):
#     name = models.CharField()
#     owner = models.ForeignKey(ProfileModel)

# class WatchListEntriesModel(models.Model):
#     company = models.ForeignKey(CompanyModel)
#     watch_list = models.ForeignKey(WatchListModel)

# class DesiredPriceModel(models.Model):
#     company = models.ForeignKey(CompanyModel, on_delete=models.DO_NOTHING)
#     desired_price = models.FloatField()
#     desired_pe = models.FloatField()
