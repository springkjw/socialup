# -*- coding: utf-8 -*-
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    user_email = forms.EmailField()
    order = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['user_type'].label = '회원분류'
        self.fields['user_email'].label = '이메일'
        self.fields['user_email'].widget.attrs['readonly'] = True
        self.fields['order'].label = '주문번호'

        self.fields['title'].label = '제목'
        self.fields['message'].label = '내용'
        self.fields['file'].label = '첨부파일'

    class Meta:
        model = Contact
        fields = ['user_type', 'user_email', 'order', 'title', 'message', 'file', ]

        widgets = {
            'user_type': forms.RadioSelect(),
        }
