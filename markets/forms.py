# -*-coding: utf-8 -*-
from django import forms
from .models import Product, Variation, product_type, sns_type, product_target
from socials.models import Sns
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(
            attrs={
                'placeholder': '최소 10글자 / 최대 40글자'
            }
        )

        self.fields['workContent'].widget = forms.TextInput(
            attrs={
                'placeholder': '기본가 작업 설명 (예:1회성 포스팅)'
            }
        )

        self.fields['workingDay'].widget = forms.TextInput(
            attrs={
                'placeholder': '기본가 작업일'
            }
        )
        self.fields['influence'].widget = forms.TextInput(
            attrs={
                'placeholder': '예시) 팔로워 10만명, 일평균 방문자수 8천명 등'
            }
        )

    class Meta:
        model = Product
        fields = (
        'title', 'image', 'description', 'workContent', 'workingDay', 'required', 'refund', 'influence', 'command',)
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
        }


class VariationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(VariationForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = ''
        self.fields['price'].label = ''
        self.fields['is_default'].label = ''

    class Meta:
        model = Variation
        fields = ('title', 'price', 'is_default',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'variation_title',
                                            'placeholder': '옵션 이름'}),
            'price': forms.TextInput(attrs={'class': 'variation_price'}),
        }


class TagForm(forms.Form):
    tag = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=product_type,
        label='',
    )


class TypeForm(forms.Form):
    type = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=sns_type,
        label='',
    )


class TargetForm(forms.Form):
    target = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=product_target,
        label='',
    )


class SnsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SnsForm, self).__init__(*args, **kwargs)

        self.fields['type'].label = ''
        self.fields['url'].label = ''

    class Meta:
        model = Sns
        fields = ('type', 'url',)
