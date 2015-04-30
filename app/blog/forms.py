from django import forms

from . import models


class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = '__all__'


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = models.Subscriber
        fields = ['name', 'email', ]

