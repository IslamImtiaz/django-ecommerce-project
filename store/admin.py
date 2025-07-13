# store/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product, ProductVariant, SlideshowBanner, Announcement # Add Announcement

# (ProductVariantInline and ProductAdmin remain as they were)
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'sku', 'price_override', 'stock', 'image', 'is_active')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'display_total_stock', 'available', 'created_at', 'is_featured']
    list_filter = ['available', 'is_featured', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'available', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'category__name']
    inlines = [ProductVariantInline]
    actions = ['mark_as_available', 'mark_as_unavailable']

    def display_total_stock(self, obj):
        return obj.get_total_stock()
    display_total_stock.short_description = 'Total Stock (Variants)'

    def mark_as_available(self, request, queryset):
        queryset.update(available=True)
    mark_as_available.short_description = "Mark selected products as available"

    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_as_unavailable.short_description = "Mark selected products as unavailable"


@admin.register(Category) # Ensure this is registered for the base Category model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent_link_admin', 'product_count_admin', 'image_tag_list_admin', 'created_at', '__str__') # Added __str__ back for hierarchy view
    list_filter = ('parent', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'parent__name')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['parent']
    ordering = ('parent__name', 'name') # This ordering is still good for grouping children under parents

    def image_tag_list_admin(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 40px; max-width: 40px;" />', obj.image.url)
        return "No image"
    image_tag_list_admin.short_description = 'Image'

    def product_count_admin(self, obj):
        return obj.products.count()
    product_count_admin.short_description = '# Products'

    def parent_link_admin(self, obj):
        if obj.parent:
            link = reverse("admin:store_category_change", args=[obj.parent.pk])
            return format_html('<a href="{}">{}</a>', link, obj.parent.name)
        return "-"
    parent_link_admin.short_description = 'Parent Category'
    parent_link_admin.admin_order_field = 'parent'

@admin.register(SlideshowBanner)
class SlideshowBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_on_category_page', 'display_on_homepage', 'image_preview_list', 'is_active', 'display_order', 'updated_at') # Added display_on_homepage
    list_filter = ('is_active', 'display_on_homepage', 'display_on_category_page', 'updated_at') # Added display_on_homepage
    search_fields = ('title', 'caption_title', 'caption_text', 'display_on_category_page__name')
    list_editable = ('is_active', 'display_order', 'display_on_homepage') # Added display_on_homepage
    fields = ('title', 'image', 'image_preview_form', 'caption_title', 'caption_text', 'link_url', 
              'display_on_category_page', 'display_on_homepage', 'display_order', 'is_active') # Added display_on_homepage
    readonly_fields = ('image_preview_form',)
    ordering = ('-display_on_homepage', 'display_on_category_page', 'display_order') # Prioritize homepage banners

    def image_preview_list(self, obj):
        # ... (as before)
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px; object-fit:contain;" />', obj.image.url)
        return "No image"
    image_preview_list.short_description = 'Image'

    def image_preview_form(self, obj):
        # ... (as before)
        if obj.image and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" style="max-height: 200px; max-width: 400px; object-fit:contain;" />', obj.image.url)
        return "No image uploaded yet."
    image_preview_form.short_description = 'Current Image Preview'

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'start_date', 'end_date', 'link_url', 'updated_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('message',)
    list_editable = ('is_active',)
    fields = ('message', 'link_url', 'is_active', 'start_date', 'end_date')
    ordering = ('-updated_at',)