from django import forms

from .models import *


class partyAddForm(forms.ModelForm):
    class Meta:
        model = PartyDetails
        fields = '__all__'


class productAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
