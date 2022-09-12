from django.contrib import admin

from .models import Order, Tax, Discount, Item, OrderItem


class ProductItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('price', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductItemInline]
    list_display = (
        'id',
        'total_price',
    )


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
