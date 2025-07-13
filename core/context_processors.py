# core/context_processors.py
from django.conf import settings
from decimal import Decimal
from .models import CurrencyRate

def currency(request):
    currency_code = request.session.get('currency', 'PKR')
    
    # This is the old, hardcoded rate that we use as a backup
    fallback_rate = settings.USD_TO_PKR_EXCHANGE_RATE 
    usd_to_pkr_rate = fallback_rate

    try:
        # We try to get the new, correct rate from the database
        rate_obj = CurrencyRate.objects.get(code='USD')
        usd_to_pkr_rate = rate_obj.rate_vs_pkr
        # ADD THIS LINE FOR DEBUGGING:
        print(f"DEBUG: Found rate in DB. Using rate: {usd_to_pkr_rate}")
    except CurrencyRate.DoesNotExist:
        # ADD THIS LINE FOR DEBUGGING:
        print(f"DEBUG: Rate not found in DB. Using fallback rate: {fallback_rate}")
        pass

    context_data = {
        'CURRENT_CURRENCY': currency_code,
        'USD_TO_PKR_EXCHANGE_RATE': usd_to_pkr_rate,
    }
    
    return context_data