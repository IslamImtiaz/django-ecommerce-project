# ecommerce_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from store import views as store_views

# Import LoginView and your custom form
from django.contrib.auth import views as auth_views # Import auth_views
from accounts.forms import CustomLoginForm # Import your custom login form

urlpatterns = [
    path('admin/', admin.site.urls),

    # ACCOUNTS URLS
    # Use your custom login form for the login URL
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html', # Ensure this points to your login template
        authentication_form=CustomLoginForm       # Use your custom form
    ), name='login'),

    # Include other accounts URLs (like register, profile) from your accounts app
    path('accounts/', include('accounts.urls')),

    # Include other default auth URLs (logout, password change, password reset)
    # Ensure this doesn't conflict with your custom login URL name if it also defines 'login'
    # If 'django.contrib.auth.urls' defines 'login', our path above takes precedence.
    path('accounts/', include('django.contrib.auth.urls')),

    # Store App URLs
    path('store/', include('store.urls')),

    # Home Page
    path('', store_views.home_page, name='home'),

    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('utils/', include('core.urls', namespace='core')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)