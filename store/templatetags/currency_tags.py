# store/templatetags/currency_tags.py
from django import template
from django.conf import settings
from decimal import Decimal
# Import the CurrencyRate model to look up the rate from the database
from core.models import CurrencyRate 

register = template.Library()

@register.filter
def currency(value, request):
    """
    Converts a PKR value to the user's selected currency and formats it.
    This now fetches the latest rate from the database.
    Usage: {{ product.price|currency:request }}
    """
    if not isinstance(value, Decimal):
        try:
            value = Decimal(value)
        except (TypeError, ValueError):
            return value 

    currency_code = request.session.get('currency', 'PKR')

    if currency_code == 'USD':
        # --- THIS IS THE UPDATED LOGIC ---
        usd_to_pkr_rate = settings.USD_TO_PKR_EXCHANGE_RATE # Default fallback
        try:
            # Fetch the up-to-date rate from the database
            rate_obj = CurrencyRate.objects.get(code='USD')
            usd_to_pkr_rate = rate_obj.rate_vs_pkr
        except CurrencyRate.DoesNotExist:
            # If rate isn't in DB, the fallback from settings will be used
            pass

        converted_price = value / usd_to_pkr_rate
        return f"${converted_price:,.2f}"

    else: # Default to PKR
        return f"Rs {value:,.0f}"