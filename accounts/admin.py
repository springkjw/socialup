from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Seller


class UserAdmin(UserAdmin):
    list_display = ('__unicode__', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('password', 'media', 'access_token')}),
        ('Personal info', {'fields': ('email', 'name', 'phone', 'description',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)
admin.site.register(Seller)