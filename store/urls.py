# store/urls.py
from django.urls import path
from . import views

app_name = 'store'  # Application namespace

urlpatterns = [
    # Product list view (shows all products or products filtered by category)
    path('', views.product_list, name='product_list_all'), # For all products
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('search/', views.search_results, name='search_results'), # For products in a specific category

    # Product detail view
    # Using both category_slug and product_slug can ensure uniqueness and provide context
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    # Alternatively, if product slugs are globally unique, you might just use:
    # path('<slug:product_slug>/', views.product_detail, name='product_detail'),
    # For now, let's go with category_slug and product_slug for better structure.
]