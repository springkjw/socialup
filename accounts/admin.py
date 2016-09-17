from django.contrib import admin
from .models import MyUser, Seller


class UserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('password', 'media',)}),
        ('Personal info', {'fields': ('email', 'name', 'phone', 'description',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)
admin.site.register(Seller)