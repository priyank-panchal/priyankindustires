import datetime

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import *
from .models import *
from datetime import date
from num2words import num2words
from django.db import connection


def index(request):
    party = PartyDetails.objects.all().count()
    now = datetime.datetime.now()
    total_income = BillDetails.objects.filter(date__year = now.year , date__month=now.month).aggregate(total_income=Sum('gst_without'))['total_income']
    orders = BillDetails.objects.filter(date__year = now.year , date__month=now.month).aggregate(orders=Count('id'))['orders']
    monthProfits = BillDetails.objects.annotate(month=TruncMonth('date')).values('month').annotate(month_wise=Sum('gst_without')).order_by('month').values('month','month_wise')
    context={
        'party':party,
        'order':orders,
        'total_income':total_income,
        'monthProfits':monthProfits
    }

    return render(request, 'Dashbord.html',context)


def partyDetails(request):
    return render(request, "Party_Details.html")


class partyAdd(SuccessMessageMixin, CreateView):
    form_class = partyAddForm
    success_message = "Submitted data created successfully"
    error_message = 'GST number should be unique'
    template_name = "Party_Add.html"
    success_url = "/partyAdd"

    def form_invalid(self, form):
        print(form.cleaned_data)
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class partyShow(ListView):
    model = PartyDetails
    template_name = 'Party_Details.html'


class productAdd(SuccessMessageMixin, CreateView):
    form_class = productAddForm
    success_message = "Submitted data created successfully"
    template_name = "product_add.html"
    success_url = "/productDetails"
    error_message = 'Product Name should be unique'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class productShow(ListView):
    model = Product
    template_name = 'product_details.html'


def invoicePrint(request, pk):
    productsBill = ProductSelling.objects.filter(billDetails=pk)
    billDetails = BillDetails.objects.get(id=pk)
    grand_total = billDetails.total_amount
    grand_total = num2words(grand_total)
    values = ProductSelling.objects.filter(billDetails=pk).count()
    final = 9 - values
    lst = []
    for i in range(1, final + 1):
        lst.append(i)
    context = {
        'data': productsBill,
        'details': billDetails,
        'words': grand_total.capitalize(),
        'looping': lst
    }

    return render(request, 'invoice-special.html', context)


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
        return JsonResponse({"resp": billDetails.id})


class invoiceShow(ListView):
    model = BillDetails
    template_name = 'InvoiceSelect.html'


class PartyWiseProfit(ListView):
    model = BillDetails
    template_name = 'Party-wise-profit.html'


def invoiceSearchNo(request, pk):
    data = list(BillDetails.objects.filter(invoice_no=pk).values())
    return JsonResponse({"party": data})


def invoiceSearchByDate(request, start, end):
    data = list(BillDetails.objects.filter(date__range=[start, end]).values())
    return JsonResponse({"party": data})


def searchByParty(request, start, end):
    data = list(BillDetails.objects.filter(date__range=[start, end]).values())
    partyExists = []
    dict = {}
    for i in range(0, len(data)):
        if data[i]['party_id'] in partyExists:
            dict[data[i]['party_id']][0] += data[i]['gst_without']
        else:
            partyExists.append(data[i]['party_id'])
            print(data[i]['party_id'])
            Party = PartyDetails.objects.get(id=data[i]['party_id'])
            dict[i] = [data[i]['gst_without'], Party.party_name,Party.gst_no]
            print(dict)
    return JsonResponse({"party": dict})
