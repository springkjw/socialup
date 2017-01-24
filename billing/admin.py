from django.contrib import admin
from .models import Point, PointTransaction, PointHistory, Order, OrderItem, Mileage, MileageHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ]

    class Meta:
        model = Order

class PointAdmin(admin.ModelAdmin):
    list_display = ('user', '__unicode__', 'timestamp')


class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'amount', 'created')


class PointHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')

class MileageAdmin(admin.ModelAdmin):
    list_display = ('user', '__unicode__', 'timestamp')

class MileageHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'timestamp')


admin.site.register(Point, PointAdmin)
admin.site.register(PointTransaction, PointTransactionAdmin)
admin.site.register(PointHistory, PointHistoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Mileage)
admin.site.register(MileageHistory)
