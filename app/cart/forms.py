from django import forms

from cart import models


class ProductReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.ProductReview
        fields = ['rating', 'comment', ]


class ShopReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.ShopReview
        fields = ['rating', 'comment', ]

