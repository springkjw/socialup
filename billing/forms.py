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
        #self.fields['review'] = forms.Textarea
        self.fields['rating'] = forms.ChoiceField(widget=forms.RadioSelect(attrs={'type': 'radio'}), choices=(('1',1),('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9),('10',10)))


    class Meta:
        model = ProductReview
        fields = (
            'contents_satisfy','ad_satisfy','kind_satisfy', 'rating', 'review'
        )