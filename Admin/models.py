from django.db import models


class PartyDetails(models.Model):
    gst_no = models.CharField(max_length=17)
    state = models.CharField(max_length=30)
    party_name = models.CharField(max_length=30)
    address = models.TextField()
    phone_no = models.CharField(max_length=12)


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    hsn_code = models.CharField(max_length=8)
    per = models.CharField(max_length=8)


class BillDetails(models.Model):
    invoice_no = models.CharField(max_length=28)
    cgst = models.FloatField(default=0.0)
    sgst = models.FloatField(default=0.0)
    igst = models.FloatField(default=0.0)
    date = models.DateField()
    total_amount = models.FloatField()
    party = models.ForeignKey(
        PartyDetails, on_delete=models.CASCADE)
    gst_without = models.FloatField()
    round_off = models.FloatField()
    time = models.TimeField(auto_now=True)


class ProductSelling(models.Model):
    amount = models.FloatField(null=True,blank=True)
    qty = models.IntegerField()
    rate = models.IntegerField(default=0)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    billDetails = models.ForeignKey(
        BillDetails, on_delete=models.CASCADE)
