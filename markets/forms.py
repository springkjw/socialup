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
from django.utils.safestring import mark_safe
from django.forms import widgets


#u'''<img src="/static/img/fasion.png">%s''' % (super(TagWidget, self).render(name, value, attrs))
class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['follower_num'].widget = forms.TextInput(
            attrs={
                'placeholder': '팔로워수'
            }
        )
        self.fields['follower_visit_num'].widget = forms.TextInput(
            attrs={
                'placeholder': '일평균방문자수'
            }
        )
        self.fields['follower_friends_num'].widget = forms.TextInput(
            attrs={
                'placeholder': '친구수'
            }
        )
        self.fields['sns_type'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=sns_type_list)
        self.fields['sns_additional_info'] = forms.ChoiceField(widget=forms.RadioSelect, choices=sns_additional_info_list, initial='individual')
        self.fields['sex'] = forms.ChoiceField(widget=forms.RadioSelect, choices=(('male','남자'),('female','여자')), initial='female')
        #self.fields['is_url_open'] = forms.BooleanField(label='',default=True)
        self.fields['message_to_buyer'] = forms.CharField(widget=forms.Textarea(
                attrs={'placeholder':'포스팅불가능 업종, A/S규정, 진행방법등','cols':'100'
                }
            ), required=False
        )
        self.fields['oneline_intro'] = forms.CharField(widget=forms.TextInput(
            attrs={'placeholder':'SNS특징을 30자 이내로 써주세요.'
        }))
        self.fields['message_to_admin'] = forms.CharField(widget=forms.Textarea(
            attrs={'placeholder': '구매자에겐 보이지 않습니다.','cols':'105'
                   }
            ), required=False
        )
        self.fields['description'] = forms.CharField(widget=SummernoteWidget(
            attrs={'width': '100%'}
            )
        )


    class Meta:
        model = Product
        fields = (
            'sns_type',
            'sns_additional_info',
            'sex',
            'is_url_open',
            'sns_url',
            'follower_num',
            'follower_visit_num',
            'follower_friends_num',
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


def validate_tag(value):
    if(len(value)>5):
        raise forms.ValidationError('select no more thant 5')


class TagForm(forms.Form):
    tag = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=product_tag_list,
        #validators=[validate_tag]
    )
    """
    def clean_tag(self):
        if len(self.cleaned_data['tag'])>5:
            print('hi')
            raise forms.ValidationError('select no more than 5')
        return self.cleaned_data['tag']
    """


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
