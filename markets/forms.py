# -*-coding: utf-8 -*-
# django import
from django import forms

# app import
from .models import (
    Product,
    Variation,
    product_type,
    sns_type,
    product_target,
)
from django_summernote.widgets import (
    SummernoteWidget,
    SummernoteInplaceWidget,
)


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(
            attrs={
                'placeholder': '최소 10글자 / 최대 40글자'
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
            'title', 'image', 'description', 'required', 'refund', 'influence', 'command',)
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
            'image': forms.FileInput(),
        }


class VariationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(VariationForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = ''
        self.fields['price'].label = ''
        self.fields['is_default'].label = ''
        self.fields['day'].label = ''

    class Meta:
        model = Variation
        fields = ('title', 'price', 'is_default', 'day',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'variation_title',
                                            'placeholder': '옵션 이름'}),
            'price': forms.TextInput(attrs={'class': 'variation_price'}),
            'day': forms.TextInput(attrs={'class': 'variation_day',
                                          'placeholder': '옵션 구매 시 추가 일수'})
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


class SnsTypeForm(forms.Form):
    sns = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=sns_type,
        label='',
    )


class SnsForm(forms.Form):
    url = forms.URLField(
        required=True,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '주소 공개시 광고주의 신뢰도가 높아집니다.'
            }
        )
    )
