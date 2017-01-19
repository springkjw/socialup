from django.contrib import admin
from .models import MyUser, Seller, SellerAccount, Profit, MyUserThumbnail, Withdrawal

class ThumbnailInline(admin.TabularInline):
	extra = 1
	model = MyUserThumbnail

class UserAdmin(admin.ModelAdmin):
	inlines = [ThumbnailInline, ]

	list_display = ('__unicode__', 'is_active', 'is_admin', )
	list_filter = ('is_admin', 'is_active')
	fieldsets = (
	    (None, {'fields': ('password', 'media',)}),
	    ('Personal info', {'fields': ('email', 'name', 'phone',
									  'description', 'sex', 'address',
									  'job', 'birth_year', 'agree_purchase_info_email')}),
	    ('Permissions', {'fields': ('is_admin', 'is_active')}),
	)
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)
admin.site.register(Seller)
admin.site.register(SellerAccount)
admin.site.register(Profit)
admin.site.register(Withdrawal)