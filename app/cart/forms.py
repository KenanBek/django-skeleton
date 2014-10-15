from django import forms

import models


class ShopReviewForm(forms.ModelForm):
    class Meta:
        model = models.ShopReview
        fields = '__all__'

