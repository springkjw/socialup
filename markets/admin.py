# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Product, ProductTag


class TaggedItemInline(GenericTabularInline):
    model = ProductTag
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline, ]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
