from dataclasses import field
from pyexpat import model
from django import forms
from django.forms.widgets import TextInput
from .models import *
from django.forms import Textarea


class partyAddForm(forms.ModelForm):
    class Meta:
        model = PartyDetails
        fields = '__all__'

    def clean_gst_no(self):
        gst_no = self.cleaned_data.get('gst_no')
        if PartyDetails.objects.filter(gst_no=gst_no).exists():
            raise forms.ValidationError("GST Number Should be unique")
        return gst_no


class productAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(productAddForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_product_name(self):
        product = self.cleaned_data.get('product_name')
        if Product.objects.filter(product_name=product).exists():
            raise forms.ValidationError("Product Should be unique")
        return product


class updateBill(forms.ModelForm):
    class Meta:
        model = BillDetails
        fields = '__all__'


class updatePurchase(forms.ModelForm):
    class Meta:
        model = PurchaseDetails
        fields = '__all__'


class updateParty(forms.ModelForm):
    class Meta:
        model = PartyDetails
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(updateParty, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class productUpdates(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(productUpdates, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreditForm(forms.ModelForm):
    class Meta:
        model = Payment_by
        fields = ['pay', 'payament_mode']

    def __init__(self, *args, **kwargs):
        super(CreditForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
