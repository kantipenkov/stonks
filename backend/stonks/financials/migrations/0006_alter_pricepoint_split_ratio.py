# Generated by Django 4.0 on 2022-01-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0005_alter_pricepoint_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricepoint',
            name='split_ratio',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
