from django import forms

from .models import *


class partyAddForm(forms.ModelForm):
    class Meta:
        model = PartyDetails
        fields = '__all__'

    def clean_gst_no(self):
        gst_no = self.cleaned_data.get('gst_no')
        if PartyDetails.objects.filter(gst_no=gst_no).exists():
            raise forms.ValidationError("Gst Number Should be unique")
        return gst_no


class productAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_product_name(self):
        product = self.cleaned_data.get('product_name')
        if Product.objects.filter(product_name=product).exists():
            raise forms.ValidationError("Product Should be unique")
        return product
