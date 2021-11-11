# Generated by Django 3.2.9 on 2021-11-11 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('ticker', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('industry', models.CharField(max_length=100)),
                ('sector', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyIncomeStatements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reported', models.DateField()),
                ('report_type', models.CharField(choices=[('A', 'Annual'), ('Q', 'Quarterly')], max_length=2)),
                ('gross_profit', models.BigIntegerField()),
                ('total_revenue', models.BigIntegerField()),
                ('cost_of_revenue', models.BigIntegerField()),
                ('cost_of_goods_and_services_sold', models.BigIntegerField()),
                ('operating_income', models.BigIntegerField()),
                ('selling_general_and_administrative', models.BigIntegerField()),
                ('rnd', models.BigIntegerField()),
                ('operating_expences', models.BigIntegerField()),
                ('investment_income_net', models.BigIntegerField()),
                ('net_interest_income', models.BigIntegerField()),
                ('interest_income', models.BigIntegerField()),
                ('interest_expense', models.BigIntegerField()),
                ('non_interest_income', models.BigIntegerField()),
                ('other_non_operating_income', models.BigIntegerField()),
                ('deprecation', models.BigIntegerField()),
                ('deprecation_and_amortization', models.BigIntegerField()),
                ('income_before_tax', models.BigIntegerField()),
                ('income_tax_expence', models.BigIntegerField()),
                ('interest_and_debt_expence', models.BigIntegerField()),
                ('net_income_from_continuing_operations', models.BigIntegerField()),
                ('comprehensive_incom_net_of_tax', models.BigIntegerField()),
                ('ebit', models.BigIntegerField()),
                ('ebitda', models.BigIntegerField()),
                ('net_income', models.BigIntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finansials.company')),
            ],
            options={
                'ordering': ['date_reported'],
            },
        ),
    ]
