# core/management/commands/update_rates.py
import requests
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import CurrencyRate

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = '97fd3faca681d47d2143be30' 
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

class Command(BaseCommand):
    help = 'Fetches and updates currency exchange rates from an external API.'

    def handle(self, *args, **options):
        self.stdout.write('Fetching currency exchange rates...')
        
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()

            if data.get('result') == 'success':
                rates = data.get('conversion_rates')
                # The rate from the API for PKR against the base (USD)
                pkr_rate_vs_usd = Decimal(rates.get('PKR'))
                
                if pkr_rate_vs_usd:
                    rate_obj, created = CurrencyRate.objects.update_or_create(
                        code='USD',
                        defaults={'rate_vs_pkr': pkr_rate_vs_usd}
                    )
                    
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created USD rate: {pkr_rate_vs_usd}'))
                    else:
                        # CORRECTED THIS LINE:
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated USD rate: {pkr_rate_vs_usd}'))
                else:
                    self.stderr.write(self.style.ERROR('PKR rate not found in API response.'))

            else:
                self.stderr.write(self.style.ERROR(f"API request failed: {data.get('error-type')}"))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'HTTP Request failed: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An unexpected error occurred: {e}'))