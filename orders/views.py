# orders/views.py
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from store.models import ProductVariant

# def order_create(request):
#     cart = Cart(request)
#     if not cart: # Redirect if cart is empty
#         return redirect('store:product_list_all')

#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic(): # Use a transaction block for atomicity
#                     # First, validate that all items in the cart are still in stock
#                     for item in cart:
#                         variant = ProductVariant.objects.get(id=item['variant'].id) # Re-fetch to get latest stock
#                         if variant.stock < item['quantity']:
#                             # If any item is out of stock, raise an error to abort the transaction
#                             raise ValueError(f"Sorry, '{variant.product.name}' is out of stock.")

#                     # If all items are in stock, proceed to create the order
#                     order = form.save(commit=False)
#                     if request.user.is_authenticated:
#                         order.user = request.user
#                     order.save() # Order is saved
                    
#                     # Now, create OrderItems and update the stock for each item
#                     for item in cart:
#                         OrderItem.objects.create(order=order,
#                                                  product_variant=item['variant'],
#                                                  price=item['price'],
#                                                  quantity=item['quantity'])
#                         # Update stock using an F() expression to prevent race conditions
#                         variant = item['variant']
#                         variant.stock = F('stock') - item['quantity']
#                         variant.save()
            
#             except ValueError as e:
#                 # Handle the stock error gracefully
#                 messages.error(request, str(e)) # Show the specific stock error message
#                 return redirect('cart:cart_detail') # Redirect back to the cart

#             # If everything was successful...
#             # Clear the cart
#             cart.clear()
            
#             # --- START: SEND CONFIRMATION EMAIL ---
#             subject = f'E-Store Order Confirmation - #{order.id}'
#             from_email = settings.DEFAULT_FROM_EMAIL
#             to_email = [order.email]
            
#             # Prepare context for email templates (request is needed for our currency filter)
#             email_context = {'order': order, 'request': request}
            
#             # Render the HTML and plain text versions of the email
#             html_message = render_to_string('orders/email/confirmation_email.html', email_context)
#             plain_message = strip_tags(html_message) # Create a plain-text version from the HTML

#             try:
#                 send_mail(
#                     subject,
#                     plain_message,
#                     from_email,
#                     to_email,
#                     html_message=html_message
#                 )
#             except Exception as e:
#                 # Log the error but don't crash the page. The user's order is still successful.
#                 print(f"Error sending confirmation email for order {order.id}: {e}")
#             # --- END: SEND CONFIRMATION EMAIL ---
            
#             # Render the "created" page as before
#             return render(request,
#                           'orders/order/created.html',
#                           {'order': order})
#     else: # GET request
#         form = OrderCreateForm()
#         # Pre-fill form if user is logged in
#         if request.user.is_authenticated and hasattr(request.user, 'profile'):
#             profile = request.user.profile
#             initial_data = {
#                 'first_name': request.user.first_name or '',
#                 'last_name': request.user.last_name or '',
#                 'email': request.user.email,
#                 'address': profile.address_line_1,
#                 'postal_code': profile.postal_zip_code,
#                 'city': profile.city,
#                 'country': profile.country
#             }
#             form = OrderCreateForm(initial=initial_data)

#     context = {'cart': cart, 'form': form}
#     return render(request, 'orders/order/create.html', context)



# orders/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from urllib.parse import quote_plus
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from store.models import ProductVariant

def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('store:product_list_all')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # This logic for saving the order and updating stock is correct
                    order = form.save(commit=False)
                    if request.user.is_authenticated:
                        order.user = request.user
                    order.save()
                    
                    for item in cart:
                        OrderItem.objects.create(order=order, product_variant=item['variant'], price=item['price'], quantity=item['quantity'])
                        variant = item['variant']
                        variant.stock = F('stock') - item['quantity']
                        variant.save()
            
            except ValueError as e:
                messages.error(request, str(e))
                return redirect('cart:cart_detail')

            # --- WHATSAPP MESSAGE LOGIC ---
            
            customer_name = f"{order.first_name} {order.last_name}"
            company_name = "Attire and Co"
            
            items_list = []
            for item in cart:
                variant = item['variant']
                product_name = variant.product.name
                variant_details = []
                if variant.size: variant_details.append(f"Size: {variant.size}")
                if variant.color: variant_details.append(f"Color: {variant.color}")
                details_str = " (" + ", ".join(variant_details) + ")" if variant_details else ""
                items_list.append(f"• {product_name}{details_str} × {item['quantity']}")
            items_str = "\n".join(items_list)
            
            total_str = f"{order.get_total_cost():.2f}"
            delivery_address_parts = [part for part in [order.address, f"{order.city}, {order.postal_code}", order.country] if part]
            delivery_address = "\n".join(delivery_address_parts)

            # --- UPDATED: Message formatted with bold text and no emojis ---
            final_message = (
                f"*Hi {customer_name}*,\n\n"
                f"Your order #{order.id} from {company_name} is confirmed.\n\n"
                f"*Items:*\n{items_str}\n\n"
                f"*Total:* {total_str}\n\n"
                f"Your order will arrive in 3 to 7 business days.\n"
                f"You will get another message with a tracking number and link once your order is shipped.\n\n"
                f"*Delivery Address:*\n{delivery_address}\n\n"
                f"*Order ID:* {order.id}"
            )
            
            encoded_message = quote_plus(final_message)
            whatsapp_number = settings.WHATSAPP_BUSINESS_NUMBER
            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
            
            cart.clear()
            return redirect(whatsapp_url)

    else: # GET request
        form = OrderCreateForm()
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = { 
                'first_name': request.user.first_name or '', 
                'last_name': request.user.last_name or '', 
                'email': request.user.email, 
                'address': profile.address_line_1, 
                'postal_code': profile.postal_zip_code, 
                'city': profile.city, 
                'country': profile.country 
            }
            form = OrderCreateForm(initial=initial_data)

    context = {'cart': cart, 'form': form}
    return render(request, 'orders/order/create.html', context)