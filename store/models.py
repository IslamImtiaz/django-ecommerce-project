# store/models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg # Import Avg for calculating average
from django.conf import settings # Import settings to get AUTH_USER_MODEL
# from django.contrib.auth.models import User # Already there if you added it
from django.templatetags.static import static 

class Category(models.Model):
    # ... (Category model remains the same as before) ...
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique URL-friendly identifier for the category.")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, help_text="Leave blank if this is a top-level category.")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, help_text="Unique URL-friendly identifier for the product.")
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, help_text="Main product image or default for variants.")
    description = models.TextField(blank=True)
    specifications = models.TextField(blank=True, help_text="Enter product specifications, perhaps as bullet points or key-value pairs.")
    
    # Price on Product can be a base/default price or might be entirely managed by variants
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price for the product. Variants can override this.")
    
    # Stock on Product model is now less relevant if variants manage their own stock.
    # It could represent total stock if you want, or be removed.
    # For now, let's keep it, but note that variant stock is the primary source.
    # We can later make this a calculated field in the admin or remove it.
    # stock = models.PositiveIntegerField(default=0, help_text="Total stock (can be sum of variant stocks).")
    
    available = models.BooleanField(default=True, help_text="Is the product generally available (can be overridden by variant availability)?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, help_text="Mark as a featured product.")
    is_bestseller = models.BooleanField(default=False, db_index=True, help_text="Mark as a best-selling product.") # NEW FIELD
    # brand = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    class Meta:
        ordering = ('-created_at', 'name',)
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.category.slug, self.slug])

    # Optional: Method to get total stock from variants
    def get_total_stock(self):
        return sum(variant.stock for variant in self.variants.filter(is_active=True))

    def average_rating(self):
        # Calculate the average rating, return 0 if no reviews
        avg = self.reviews.filter(rating__gt=0).aggregate(Avg('rating'))['rating__avg']
        return avg or 0

    def review_count(self):
        return self.reviews.count()
    
    @property
    def get_display_image(self):
        """
        Returns the URL for the product's display image.
        Prioritizes the uploaded file, then the URL, then a static default.
        """
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        elif self.image_url:
            return self.image_url
        else:
            return static('images/default_product_image.png')

# New Model for Product Variations
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    # Attribute fields - for simplicity, CharFields.
    # For more complex systems, these could be ForeignKeys to AttributeOption models.
    size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., S, M, L, XL, 200g, 1kg")
    color = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Red, Blue, Green, Onyx Black")
    # Add other variant attributes as needed, e.g., material, style

    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Stock Keeping Unit for this specific variant.")
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Override product's base price for this variant. If blank, base price is used.")
    stock = models.PositiveIntegerField(default=0, help_text="Available units for this specific variant.")
    image = models.ImageField(upload_to='products/variants/%Y/%m/%d/', blank=True, null=True, help_text="Image specific to this variant.")
    is_active = models.BooleanField(default=True, help_text="Is this variant currently available/active?")

    class Meta:
        # Ensure that for a given product, the combination of size and color (and other attributes) is unique.
        # Adjust this if you add more variant attributes.
        unique_together = [['product', 'size', 'color']] # Example: A product can't have two "Red, Medium" variants.
        ordering = ['product', 'size', 'color'] # Optional: default ordering

    def __str__(self):
        variant_name_parts = [str(self.product.name)]
        if self.size:
            variant_name_parts.append(f"Size: {self.size}")
        if self.color:
            variant_name_parts.append(f"Color: {self.color}")
        # Add other attributes to the name if they exist
        return " - ".join(variant_name_parts) + (f" (SKU: {self.sku})" if self.sku else "")

    # Method to get the actual price for this variant
    def get_price(self):
        if self.price_override is not None:
            return self.price_override
        return self.product.price

class SlideshowBanner(models.Model):
    title = models.CharField(max_length=200, help_text="Internal title for this banner (e.g., 'Men's Summer Sale').")
    image = models.ImageField(upload_to='slideshow_banners/%Y/%m/', help_text="Banner image (e.g., 1200x400 pixels).")
    caption_title = models.CharField(max_length=100, blank=True, null=True, help_text="Title text to display on the banner.")
    caption_text = models.CharField(max_length=255, blank=True, null=True, help_text="Short descriptive text on the banner.")
    link_url = models.URLField(blank=True, null=True, help_text="Full URL this banner should link to (e.g., a promotion page).")
    
    display_on_category_page = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='categorypage_banners', # Changed related_name to avoid conflict if you reuse 'slideshow_banners'
        null=True, blank=True,
        help_text="Select a parent category page where this banner should appear."
    )
    display_on_homepage = models.BooleanField( # NEW FIELD
        default=False, 
        db_index=True,
        help_text="Show this banner on the homepage slideshow."
    )
    
    display_order = models.PositiveIntegerField(default=0, help_text="Order of display in the slideshow (0 first).")
    is_active = models.BooleanField(default=True, help_text="Is this banner currently active and should be displayed?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_on_homepage', 'display_on_category_page', 'display_order', '-created_at'] # Updated ordering
        verbose_name = "Slideshow Banner"
        verbose_name_plural = "Slideshow Banners"

    def __str__(self):
        return self.title
    
class Announcement(models.Model):
    message = models.TextField(help_text="The announcement message. Emojis are supported. Keep it concise for the strip.")
    link_url = models.URLField(max_length=255, blank=True, null=True, help_text="Optional: URL to link the announcement to.")
    is_active = models.BooleanField(default=False, db_index=True, help_text="Check this to make the announcement visible on the site.")
    
    # Optional: Scheduling for the announcement
    start_date = models.DateTimeField(null=True, blank=True, help_text="When this announcement should start appearing (optional).")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When this announcement should stop appearing (optional).")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at'] # Show most recently updated first in admin
        verbose_name = "Site Announcement"
        verbose_name_plural = "Site Announcements"

    def __str__(self):
        return self.message[:75] + '...' if len(self.message) > 75 else self.message

    @classmethod
    def get_current(cls):
        """
        Gets the current active announcement.
        Prioritizes announcements with valid start/end dates.
        Falls back to any active announcement if scheduling is not used or dates are out of range.
        """
        now = timezone.now()
        # Try to find an announcement with active scheduling
        announcement = cls.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-updated_at').first()

        if not announcement:
            # Fallback: if no scheduled announcement is active, try one without specific start/end dates
            # or where start_date is past and end_date is null (ongoing from start_date)
            # or where start_date is null and end_date is in future (active until end_date)
            # or simply any active one if specific date logic is too complex for simple cases
            announcement = cls.objects.filter(
                is_active=True,
                start_date__isnull=True, # No start date, or start date is past
                end_date__isnull=True    # No end date, or end date is future
            ).exclude( # Exclude those that have specific dates but are not current
                start_date__gt=now 
            ).exclude(
                end_date__lt=now
            ).order_by('-updated_at').first()
        
        if not announcement: # Simplified fallback if above is too complex or doesn't catch all cases
            announcement = cls.objects.filter(is_active=True).order_by('-updated_at').first()

        return announcement
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews', on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Rate the product from 1 to 5.")
    comment = models.TextField(max_length=1000, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # A user can only write one review per product
        unique_together = ('product', 'user')
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'