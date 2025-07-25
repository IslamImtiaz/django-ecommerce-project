# Generated by Django 5.1.5 on 2025-06-06 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='ISO currency code (e.g., USD, EUR).', max_length=3, unique=True)),
                ('rate_vs_pkr', models.DecimalField(decimal_places=5, help_text='Exchange rate against the base currency (PKR).', max_digits=15)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
