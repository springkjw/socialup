from django.contrib import admin
from .models import ProductReview

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', '__unicode__',)

    class Meta:
        model = ProductReview


admin.site.register(ProductReview, ReviewAdmin)