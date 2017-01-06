from django.contrib import admin
from .models import Cart, CartItem, WishList


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline
    ]

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
admin.site.register(WishList)
admin.site.register(CartItem)
