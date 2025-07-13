# orders/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem

    # REMOVED the 'fields' line. Django will automatically use the readonly_fields.
    readonly_fields = ('product_variant_display', 'price', 'quantity', 'get_cost_display')
    extra = 0
    can_delete = False # Prevent deleting items from a created order

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'product_variant', 
            'product_variant__product'
        )

    def product_variant_display(self, obj):
        variant = obj.product_variant
        if not variant:
            return "Product Not Available"
        text_parts = [str(variant.product.name)]
        if variant.size:
            text_parts.append(f"Size: {variant.size}")
        if variant.color:
            color_swatch = format_html(
                '<span style="display: inline-block; width: 15px; height: 15px; background-color: {}; border: 1px solid #ccc; border-radius: 3px; vertical-align: middle; margin-left: 5px;"></span>',
                variant.color
            )
            color_part = format_html('Color: {}', color_swatch)
            text_parts.append(str(color_part))
        return format_html(' - '.join(text_parts))
    product_variant_display.short_description = 'Product'

    def get_cost_display(self, obj):
        return f"${obj.get_cost()}"
    get_cost_display.short_description = 'Total Cost'

# The rest of your OrderAdmin class remains the same...
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'paid', 'created_at']
    list_filter = ['paid', 'created_at', 'updated_at']
    search_fields = ('first_name', 'last_name', 'email', 'id', 'items__product_variant__product__name', 'items__product_variant__sku')
    inlines = [OrderItemInline]