# cart/forms.py
from django import forms

class CartAddProductForm(forms.Form):
    # This will hold the ID of the ProductVariant being added/updated
    variant_id = forms.IntegerField(widget=forms.HiddenInput) 
    
    # Allow quantity to be 0 for updates, but default to 1 for adding
    quantity = forms.IntegerField(
        min_value=0, # Changed from 1 to 0
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'width: 70px; text-align: center;'})
    )
    
    # This boolean allows us to either add to existing quantity or override it
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)