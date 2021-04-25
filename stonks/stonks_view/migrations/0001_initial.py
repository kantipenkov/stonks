# Generated by Django 3.1.7 on 2021-04-25 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('ticker', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WatchItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=12)),
                ('watch_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks_view.watchlist')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyEarnings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reported', models.DateField()),
                ('revenue', models.IntegerField()),
                ('operating_income', models.IntegerField()),
                ('net_income', models.IntegerField()),
                ('income_before_tax', models.IntegerField()),
                ('gross_profit', models.IntegerField()),
                ('eps', models.FloatField()),
                ('eps_diluted', models.FloatField()),
                ('ebitda', models.IntegerField()),
                ('cost_of_revenue', models.IntegerField()),
                ('interest_expence', models.IntegerField()),
                ('rnd_expences', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks_view.company')),
            ],
            options={
                'ordering': ['date_reported'],
            },
        ),
        migrations.CreateModel(
            name='CompanyCashFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reported', models.DateField()),
                ('accounts_payables', models.IntegerField()),
                ('accounts_receuvables', models.IntegerField()),
                ('acquisitions_net', models.IntegerField()),
                ('capital_expenditure', models.IntegerField()),
                ('cash_at_beginning', models.IntegerField()),
                ('cash_at_end', models.IntegerField()),
                ('change_in_work_capital', models.IntegerField()),
                ('common_stock_issued', models.IntegerField()),
                ('common_stock_repurchased', models.IntegerField()),
                ('debt_repayment', models.IntegerField()),
                ('deferred_income_tax', models.IntegerField()),
                ('deprecation_and_amortization', models.IntegerField()),
                ('dividend_paid', models.IntegerField()),
                ('free_cash_flow', models.IntegerField()),
                ('inventory', models.IntegerField()),
                ('investments_in_property', models.IntegerField()),
                ('cash_provided_by_operations', models.IntegerField()),
                ('cash_used_for_investment', models.IntegerField()),
                ('cash_by_financing', models.IntegerField()),
                ('change_in_cash', models.IntegerField()),
                ('operation_cash_flow', models.IntegerField()),
                ('other_financing_activities', models.IntegerField()),
                ('other_investing_activities', models.IntegerField()),
                ('other_non_cash_items', models.IntegerField()),
                ('other_working_capital', models.IntegerField()),
                ('purchase_of_investments', models.IntegerField()),
                ('sales_maturity_of_investments', models.IntegerField()),
                ('stock_based_compensation', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks_view.company')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reported', models.DateField()),
                ('account_payables', models.IntegerField()),
                ('cash', models.IntegerField()),
                ('cash_and_short_investments', models.IntegerField()),
                ('deferred_revenue', models.IntegerField()),
                ('goodwill', models.IntegerField()),
                ('intangible_assets', models.IntegerField()),
                ('long_term_investments', models.IntegerField()),
                ('long_term_debt', models.IntegerField()),
                ('net_debt', models.IntegerField()),
                ('net_receivables', models.IntegerField()),
                ('other_assets', models.IntegerField()),
                ('other_current_assets', models.IntegerField()),
                ('other_current_liabilities', models.IntegerField()),
                ('other_liabilities', models.IntegerField()),
                ('other_non_current_assets', models.IntegerField()),
                ('other_non_current_liabilities', models.IntegerField()),
                ('property_plant_equipment_net', models.IntegerField()),
                ('retained_earnings', models.IntegerField()),
                ('short_term_debt', models.IntegerField()),
                ('short_term_investments', models.IntegerField()),
                ('tax_assets', models.IntegerField()),
                ('total_assets', models.IntegerField()),
                ('total_current_assets', models.IntegerField()),
                ('total_current_liabilities', models.IntegerField()),
                ('total_debt', models.IntegerField()),
                ('total_investments', models.IntegerField()),
                ('total_liabilities', models.IntegerField()),
                ('total_non_current_assets', models.IntegerField()),
                ('total_non_current_liabilities', models.IntegerField()),
                ('total_stockholders_equity', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stonks_view.company')),
            ],
        ),
    ]
