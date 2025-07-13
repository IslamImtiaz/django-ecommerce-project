# store/views.py
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, SlideshowBanner
import json # Import the json library
from django.db.models import Q
from .models import Category, Product, Review # Add Review
from .forms import ReviewForm # Add ReviewForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404




def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product,
                                category__slug=category_slug,
                                slug=product_slug,
                                available=True)


    # Review Logic
    reviews = product.reviews.all()
    review_form = ReviewForm()
    user_has_reviewed = False
    if request.user.is_authenticated:
        if reviews.filter(user=request.user).exists():
            user_has_reviewed = True

    if request.method == 'POST' and request.user.is_authenticated and not user_has_reviewed:
        # This part handles the submission of a new review
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.user = request.user
            new_review.save()
            messages.success(request, 'Thank you! Your review has been submitted.')
            # Redirect to the same page to show the new review and prevent re-submission
            return redirect(product.get_absolute_url())
        else:
            messages.error(request, 'There was an error with your submission. Please check the form.')
            

    # Get active variants with stock for selection
    active_variants = product.variants.filter(is_active=True) # Keep all active, JS will handle stock check

    # Prepare data for frontend
    # Unique, sorted lists of available attributes for creating selection UI
    # Consider only attributes from variants that are active
    available_colors_qs = active_variants.exclude(color__isnull=True).exclude(color__exact='').order_by('color').values_list('color', flat=True).distinct()
    available_sizes_qs = active_variants.exclude(size__isnull=True).exclude(size__exact='').order_by('size').values_list('size', flat=True).distinct()
    
    available_colors = sorted(list(available_colors_qs))
    available_sizes = sorted(list(available_sizes_qs))

    # Pass all active variant data as JSON for JavaScript to use
    variants_data = []
    for v in active_variants:
        variant_info = {
            'id': v.id,
            'size': v.size or "", # Ensure None becomes empty string for JS
            'color': v.color or "", # Ensure None becomes empty string for JS
            'price': str(v.get_price()), # Convert Decimal to string
            'stock': v.stock,
            'sku': v.sku or "",
            'image_url': v.image.url if v.image else (product.image.url if product.image else "")
        }
        variants_data.append(variant_info)
    
    variants_json = json.dumps(variants_data)
    
    # Determine if the product has color/size options to show the sections
    has_color_options = bool(available_colors)
    has_size_options = bool(available_sizes)

    categories = Category.objects.filter(parent__isnull=True)

    context = {
        'product': product,
        'variants_json': variants_json, # All variant data for JS
        'available_colors': available_colors, # Unique colors for UI
        'available_sizes': available_sizes,   # Unique sizes for UI
        'has_color_options': has_color_options,
        'has_size_options': has_size_options,
        'categories': categories,
        'reviews': reviews,             # NEW: Pass reviews to template
        'review_form': review_form,     # NEW: Pass review form
        'user_has_reviewed': user_has_reviewed, # NEW: Pass flag
    }
    return render(request, 'store/product/detail.html', context)


def product_list(request, category_slug=None):
    current_category = None
    sidebar_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    
    products = []
    grouped_products_by_subcategory = []
    is_grouped_display_active = False
    is_current_category_a_parent = False
    slideshow_banners = [] # Initialize empty list for banners

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        
        if current_category.children.exists():
            is_current_category_a_parent = True
            # Fetch active banners for this specific parent category, ordered by display_order
            slideshow_banners = SlideshowBanner.objects.filter(
                display_on_category_page=current_category, 
                is_active=True
            ).order_by('display_order')

        subcategories_with_products = current_category.children.filter(products__available=True).distinct().order_by('name')
        if subcategories_with_products.exists():
            is_grouped_display_active = True
            for sub_cat in subcategories_with_products:
                products_in_sub = Product.objects.filter(category=sub_cat, available=True).order_by('name')
                if products_in_sub.exists():
                    grouped_products_by_subcategory.append({
                        'subcategory': sub_cat,
                        'products': products_in_sub
                    })
            if not grouped_products_by_subcategory:
                 products = Product.objects.filter(category=current_category, available=True).order_by('name')
                 is_grouped_display_active = False
        else:
            products = Product.objects.filter(category=current_category, available=True).order_by('name')
            is_grouped_display_active = False
    else:
        products = Product.objects.filter(available=True).order_by('name')
        # You could also fetch "global" banners here if display_on_category_page is None
        # slideshow_banners = SlideshowBanner.objects.filter(display_on_category_page__isnull=True, is_active=True).order_by('display_order')


    context = {
        'current_category': current_category,
        'sidebar_categories': sidebar_categories,
        'products': products,
        'grouped_products_by_subcategory': grouped_products_by_subcategory,
        'is_grouped_display_active': is_grouped_display_active,
        'is_current_category_a_parent': is_current_category_a_parent,
        'slideshow_banners': slideshow_banners, # Add banners to context
    }
    return render(request, 'store/product/list.html', context)


def home_page(request):
    homepage_banners = SlideshowBanner.objects.filter(
        is_active=True, 
        display_on_homepage=True
    ).order_by('display_order')

    featured_products = Product.objects.filter(
        available=True, 
        is_featured=True
    ).order_by('-created_at')[:10] # Get up to 10 featured products

    bestselling_products = Product.objects.filter(
        available=True,
        is_bestseller=True
    ).order_by('?')[:8] # Get up to 8, order randomly among bestsellers

    if not bestselling_products.exists():
        # If no products are marked as bestseller, show some random available products
        # Note: order_by('?') can be inefficient on very large databases.
        bestselling_products = Product.objects.filter(available=True).order_by('?')[:8]

    context = {
        'homepage_banners': homepage_banners,
        'featured_products': featured_products,
        'bestselling_products': bestselling_products,
        # You can add more context if needed, e.g., top-level categories for a menu
        'sidebar_categories': Category.objects.filter(parent__isnull=True).order_by('name')
    }
    return render(request, 'home.html', context)

def search_results(request):
    query = request.GET.get('q', '') # Get the search query, default to empty string
    results = []
    query_searched = False

    if query:
        query_searched = True
        # Search in product name, description, and category name
        # Using distinct() to avoid duplicate results if a product matches in multiple fields
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query) | # Search in the name of the related category
            Q(variants__sku__icontains=query), # Optional: search by variant SKU
            available=True # Only search available products
        ).distinct().order_by('name') 
        # Note: Searching related fields like category__name or variants__sku can be less performant
        # on very large datasets without proper indexing or more advanced search tools.

    context = {
        'query': query,
        'results': results,
        'query_searched': query_searched, # Flag to know if a search was performed
        'sidebar_categories': Category.objects.filter(parent__isnull=True).order_by('name'), # For sidebar nav
    }
    return render(request, 'store/search_results.html', context)