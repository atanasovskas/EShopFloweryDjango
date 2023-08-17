from django.contrib import admin
from .models import *


admin.site.register(UserProfile)

class AddressAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Address,AddressAdmin)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code','name','price')
admin.site.register(Product,ProductAdmin)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','cart')

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Payment,PaymentAdmin)
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'address', 'order_status', 'date_created','total_price')
    inlines = (OrderItemAdmin,)

    def total_price(self, obj):
        return sum(item.subtotal() for item in obj.orderitem_set.all())




admin.site.register(Order, OrderAdmin)
class CartItemAdmin(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemAdmin,)
    list_display = ('id','user','total_price','display_cart_items','total_price')

    def has_change_permission(self, request, obj=None):
        return False
    def total_price(self, obj):
        return sum(item.subtotal() for item in obj.cartitem_set.all())

    def display_cart_items(self, obj):
        items = [f"{item.item.name} ({item.quantity}) - {item.subtotal()} ден." for item in obj.cartitem_set.all()]
        return ", ".join(items)

    total_price.short_description = 'Total Price'
    display_cart_items.short_description = 'Cart Items'

admin.site.register(Cart, CartAdmin)

class FavoriteItemAdmin(admin.TabularInline):
    model = FavoriteItem
    extra = 0


class FavoriteAdmin(admin.ModelAdmin):
    inlines = (FavoriteItemAdmin,)
    list_display = ('user',)

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Favorite, FavoriteAdmin)




