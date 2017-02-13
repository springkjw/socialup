# -*- coding: utf-8 -*-
from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ReportForm, self).__init__(*args, **kwargs)

        self.fields['type'].label = '신고유형'
        self.fields['bad_user_description'].label = '신고할 ID'
        self.fields['detail'].label = '신고내용'
        self.fields['file'].label = '첨부파일'

    class Meta:
        model = Report
        fields = ['type', 'bad_user_description', 'detail', 'file',]

        widgets = {
            'type': forms.Select(),
        }
