# Generated by Django 3.2.9 on 2021-11-21 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finansials', '0003_alter_companybalancereport_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycashflowreport',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_flows_reports', to='finansials.company'),
        ),
    ]
