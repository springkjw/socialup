# -*-coding: utf-8 -*-

from __future__ import unicode_literals
from django import forms
from reviews.models import ProductReview, SATISFY_CHOICES

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields['contents_satisfy'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=SATISFY_CHOICES)
        self.fields['ad_satisfy'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=SATISFY_CHOICES)
        self.fields['kind_satisfy'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=SATISFY_CHOICES)
        self.fields['rating'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=(('0.50',0.5),('1.00',1),('1.50',1.5),('2.00',2),('2.50',2.5),('3.00',3),('3.50',3.5),('4.00',4),('4.50',4.5),('5.00',5)))
        self.fields['review'] = forms.CharField(widget=forms.Textarea(attrs={'required': True, 'rows':5, 'cols':45, 'placeholder': '한글 기준 최소 5자 이상'}))

    class Meta:
        model = ProductReview
        fields = (
            'contents_satisfy','ad_satisfy','kind_satisfy', 'rating', 'review'
        )