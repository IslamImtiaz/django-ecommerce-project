from django.db import models

# Create your models here.
# core/models.py
from django.db import models

class CurrencyRate(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text="ISO currency code (e.g., USD, EUR).")
    rate_vs_pkr = models.DecimalField(max_digits=15, decimal_places=5, help_text="Exchange rate against the base currency (PKR).")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} to PKR Rate: {self.rate_vs_pkr}"