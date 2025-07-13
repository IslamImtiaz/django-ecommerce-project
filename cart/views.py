from django.shortcuts import render

# Create your views here.
# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import ProductVariant
from .cart import Cart
from .forms import CartAddProductForm # We will create this form next

@require_POST # Ensures this view can only be accessed with a POST request
def cart_add(request):
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        variant = get_object_or_404(ProductVariant, id=cd['variant_id'])
        cart.add(variant=variant,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail') # Redirect to the cart detail page

@require_POST
def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    return redirect('cart:cart_detail')

# def cart_detail(request):
#     cart = Cart(request)
#     # We'll create the update quantity form later
#     # for item in cart:
#     #     item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
#     return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_update(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    form = CartAddProductForm(request.POST) # Re-using this form
    if form.is_valid():
        cd = form.cleaned_data
        # Use the add method with override_quantity=True to update
        cart.add(variant=variant,
                 quantity=cd['quantity'],
                 override_quantity=cd['override']) # override will be True from the form
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    # Prepare form instances for each item for quantity updates
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'variant_id': item['variant'].id, # Pre-populate variant_id
            'override': True
        })
    return render(request, 'cart/detail.html', {'cart': cart})