from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def set_currency(request):
    # Get data from the form
    currency_code = request.POST.get('currency', 'PKR')
    # Check if the selected currency is valid
    if currency_code in ['PKR', 'USD']:
        # Store the selected currency in the user's session
        request.session['currency'] = currency_code

    # Redirect back to the page the user was on
    return redirect(request.META.get('HTTP_REFERER', '/'))