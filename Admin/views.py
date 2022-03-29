from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import *
from .models import *
from datetime import date


def index(request):
    return render(request, 'invoice-generate.html')


def partyDetails(request):
    return render(request, "Party_Details.html")


class partyAdd(SuccessMessageMixin, CreateView):
    form_class = partyAddForm
    success_message = "Submitted data created successfully"
    template_name = "Party_Add.html"
    success_url = "/partyAdd"


class partyShow(ListView):
    model = PartyDetails
    template_name = 'Party_Details.html'


class productAdd(SuccessMessageMixin, CreateView):
    form_class = productAddForm
    success_message = "Submitted data created successfully"
    template_name = "product_add.html"
    success_url = "/index/productDetails"


class productShow(ListView):
    model = Product
    template_name = 'product_details.html'


class invoicePrint(View):
    def get(self, request):
        return render(request, "invoice-special.html")


class invoiceBillShow(ListView):
    context_object_name = "data"
    template_name = 'order-generate.html'

    def get_queryset(self):
        context = {
            "product": Product.objects.all(),
            "partyInformation": PartyDetails.objects.all()
        }
        return context


def gstDetails(request, pk):
    party = PartyDetails.objects.filter(id=pk)
    print(list(party.values()))
    return JsonResponse({"party": list(party.values())})


def ProductOne(request, pk):
    products = Product.objects.filter(id=pk)
    print(list(products.values()))
    return JsonResponse({"product": list(products.values())})


class getInvoiceNumber(View):
    def get(self, request):

        billdetails = BillDetails.objects.all().last()
        number = 1
        if billdetails:
              number = int(billdetails.invoice_no)
              print(number)
              number += 1
        return JsonResponse({"invoiceNo": number})


class allData(View):
    def post(self, request):
        try:
            inputData = request.POST
            print(inputData)
            gstno = int(inputData.get("gstno", "0"))
            cgst = float(inputData.get("cgst", "0"))
            sgst = float(inputData.get("sgst", "0"))
            igst = float(inputData.get("igst", "0"))
            invoice_no = int(inputData.get("invoiceNumber", "0"))
            roundoff = float(inputData.get("roundoff", "0"))
            gst_without = float(inputData.get("subtotal", "0"))
            total_amount = float(inputData.get("grandtotal"))
            billDetails = BillDetails()
            billDetails.invoice_no = invoice_no
            billDetails.cgst = cgst
            billDetails.sgst = sgst
            billDetails.igst = igst
            billDetails.date = date.today()
            billDetails.total_amount = total_amount
            party = PartyDetails.objects.get(id=gstno)
            billDetails.party = party
            billDetails.gst_without = gst_without
            billDetails.round_off = roundoff
            billDetails.save()
            Productids = [int(i) for i in inputData.getlist("ProductName[]", "0")]
            qty = [int(i) for i in inputData.getlist("qty[]", "0")]
            rate = [int(i) for i in inputData.getlist("rate[]", "0")]
            amount = [float(i) for i in inputData.getlist("amount[]", '0')]
            for i in range(0, len(Productids)):
                productObjects = Product.objects.get(id=Productids[i])
                productSelling = ProductSelling()
                productSelling.amount = amount[i]
                productSelling.qty = qty[i]
                productSelling.rate = rate[i]
                productSelling.product = productObjects
                productSelling.billDetails = billDetails
                productSelling.save()
        except Exception as e:
            return JsonResponse({"resp": print(e)})
        return JsonResponse({"resp": "Succesfully insert Data"})
