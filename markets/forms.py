# -*-coding: utf-8 -*-
# django import
from django import forms

# app import
from .models import (
    Product,
    sns_type_list,
    sns_additional_info_list,
    product_tag_list
)
from accounts.models import SellerAccount

from django_summernote.widgets import (
    SummernoteWidget,
    SummernoteInplaceWidget,
)

sns_choice = (('blog', '블로그'),('facebook', '페이스북'),
              ('instagram', '인스타그램'),('kakaostory', '카카오스토리'))

sns_additional_choice = (('individual','개인'),('page','페이지'))

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['follower_num'].widget = forms.TextInput(
            attrs={
                'placeholder': '예시) 팔로워 10만명, 일평균 방문자수 8천명 등'
            }
        )
        self.fields['sns_type'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=sns_choice)
        self.fields['sns_additional_info'] = forms.ChoiceField(widget=forms.RadioSelect, choices=sns_additional_choice)
        self.fields['sex'] = forms.ChoiceField(widget=forms.RadioSelect, choices=(('male','남자'),('female','여자')))

    class Meta:
        model = Product
        fields = (
            'sns_type',
            'sns_additional_info',
            'sex',
            'is_url_open',
            'sns_url',
            'follower_num',
            #'product_tag',
            'message_to_buyer',
            'oneline_intro',
            'description',
            'price',
            'manuscript_available',
            'manuscript_price',
            'highrank_available',
            'highrank_price',
            'working_period',
            'message_to_admin'
        )
        widgets = {
            'foo': SummernoteWidget(),
            'bar': SummernoteInplaceWidget(),
            'image': forms.FileInput(),
        }


class TagForm(forms.Form):
    tag = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=product_tag_list,
        label='',
    )


class SellerAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(SellerAccountForm, self).__init__(*args, **kwargs)

        self.fields['account_name'].label = '예금주'
        self.fields['bank'].label = '은행'
        self.fields['account_number'].label = '계좌번호'
    
    class Meta:
        model=SellerAccount
        fields = ('account_name', 'bank', 'account_number',)
        widgets = {
            'account_number': forms.TextInput(
                attrs={
                        'placeholder': 'ex) 000-000-000'
                    }
                ),
        }
