# accounts/urls.py
from django.urls import path
from . import views

# accounts/urls.py
# ... (keep existing register path)
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('orders/', views.order_history, name='order_history'), # NEW: For list of all user orders
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    # Login, logout, password change/reset URLs are included from django.contrib.auth.urls
    # in the project's urls.py
]