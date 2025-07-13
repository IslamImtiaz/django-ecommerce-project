from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from orders.models import Order # Import the Order model
# accounts/views.py
# ... (keep existing register view)
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages # For displaying messages
from django.shortcuts import render, redirect, get_object_or_404

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in directly after registration
            return redirect('home')  # Redirect to a home page (we'll define this later)
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



@login_required # Ensures only logged-in users can access this view
def profile_view(request):
    # Profile is automatically created/retrieved thanks to signals
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': request.user.profile # Pass the profile for display
    }
    return render(request, 'accounts/profile_view.html', context)

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES or None, instance=request.user.profile) # request.FILES for profile_picture

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile_view') # Redirect back to the profile view page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_update.html', context)


@login_required # Ensures only logged-in users can access this page
def order_history(request):
    # Fetch all orders for the current user, most recent first
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'accounts/order_history.html', context)

@login_required
def order_detail(request, order_id):
    # Fetch the specific order, ensuring it belongs to the current user for security
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # The order object will have access to its items via the 'items' related_name
    # e.g., in the template you can do {% for item in order.items.all %}
    context = {
        'order': order
    }
    return render(request, 'accounts/order_detail.html', context)