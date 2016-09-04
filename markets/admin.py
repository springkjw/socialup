#-*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Product, ProductTag, Variation, SnsType, ProductTarget, SnsUrl


class TaggedItemInline(GenericTabularInline):
    model = ProductTag
    extra = 1


class SnsItemInline(GenericTabularInline):
    model = SnsType
    extra = 1


class TargetItemInline(GenericTabularInline):
    model = ProductTarget
    extra = 1


class UrlItemInline(GenericTabularInline):
    model = SnsUrl
    extra = 1


class VariationInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        kwargs['initial'] = [
            {'title': '기본가'},
            {'is_default': True}
        ]
        super(VariationInlineFormSet, self).__init__(*args, **kwargs)


    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass

        if count < 1:
            raise ValidationError('You must have at least one order')


class VariationInline(admin.StackedInline):
    model = Variation
    extra = 1
    formset = VariationInlineFormSet

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra


class ProductAdmin(admin.ModelAdmin):
    inlines = [VariationInline, TaggedItemInline, TargetItemInline, SnsItemInline, UrlItemInline,]

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)