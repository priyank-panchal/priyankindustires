from pyexpat import model
from django.db import models
from .ChoiceModel import PAYMENT_CHOICES


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

# sales entery are here


class BillDetails(models.Model):
    invoice_no = models.CharField(max_length=28)
    cgst = models.FloatField(default=0.0)
    sgst = models.FloatField(default=0.0)
    igst = models.FloatField(default=0.0)
    date = models.DateField()
    total_amount = models.FloatField(default=0.0)
    party = models.ForeignKey(
        PartyDetails, on_delete=models.CASCADE)
    gst_without = models.FloatField()
    round_off = models.FloatField()
    time = models.TimeField(auto_now=True)

# purchse entry are put here


class PurchaseDetails(models.Model):
    cgst = models.FloatField(default=0.0, null=True)
    sgst = models.FloatField(default=0.0, null=True)
    igst = models.FloatField(default=0.0, null=True)
    date = models.DateField(null=True)
    total_amount = models.FloatField(default=0.0, null=True)
    party = models.ForeignKey(
        PartyDetails, on_delete=models.CASCADE)
    gst_without = models.FloatField(null=True)
    round_off = models.FloatField(null=True)
    time = models.TimeField(auto_now=True)

# payment related entry are put here


class Payment_by(models.Model):
    payament_mode = models.CharField(
        max_length=7, choices=PAYMENT_CHOICES, default="Cash")
    pay = models.FloatField(null=True)
    billDetails = models.ForeignKey(
        BillDetails, on_delete=models.CASCADE, null=True, related_name="bill")
    purchaseDetail = models.ForeignKey(
        PurchaseDetails, on_delete=models.CASCADE, null=True, related_name="purchase")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payament_mode


# sales and purchse all the product entrie are put here


class ProductSelling(models.Model):
    CHOICE = (
        ("1", "Selling"),
        ("2", "Purchasing")
    )
    amount = models.FloatField(null=True, blank=True)
    qty = models.FloatField(default=0.0, null=True)
    rate = models.FloatField(default=0.0, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    billDetails = models.ForeignKey(
        BillDetails, on_delete=models.CASCADE, null=True)
    purchaseDetails = models.ForeignKey(
        PurchaseDetails, on_delete=models.CASCADE, null=True)
    choice = models.CharField(
        max_length=2, choices=CHOICE, default="2", null=True)
