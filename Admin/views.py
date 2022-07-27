import datetime
from re import template
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncMonth, ExtractMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import *
from .models import *
from datetime import date
from num2words import num2words
from django.template.loader import get_template
import pandas as pd
from django.views.generic.edit import UpdateView


def index(request):
    party = PartyDetails.objects.all().count()
    now = datetime.datetime.now()
    total_income = \
        BillDetails.objects.filter(date__year=now.year, date__month=now.month).aggregate(
            total_income=Sum('gst_without'))[
            'total_income']
    gst_pay = BillDetails.objects.filter(date__year=now.year, date__month=now.month).aggregate(
        gst=Sum(F('cgst') + F('sgst') + F('igst')))['gst']
    orders = BillDetails.objects.filter(date__year=now.year, date__month=now.month).aggregate(orders=Count('id'))[
        'orders']
    monthProfits = BillDetails.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        totalprofit=Sum('gst_without')).reverse()[:12]
    dataframe = pd.DataFrame(monthProfits.values('totalprofit', 'month'))
    totalprofit = dataframe.totalprofit.tolist()
    months = dataframe.month.tolist()
    context = {
        'party': party,
        'order': orders,
        'gst_pay': gst_pay,
        'total_income': total_income,
        'monthProfits': monthProfits,
        'totalprofit': totalprofit,
        'months': months
    }
    return render(request, 'Dashbord.html', context)


def partyDetails(request):
    return render(request, "Party_Details.html")


class partyAdd(SuccessMessageMixin, CreateView):
    form_class = partyAddForm
    success_message = "Submitted data created successfully"
    error_message = 'GST number should be unique'
    template_name = "Party_Add.html"
    success_url = "/partyAdd"

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class partyShow(ListView):
    model = PartyDetails
    template_name = 'Party_Details.html'
    ordering = ['party_name']


class productAdd(SuccessMessageMixin, CreateView):
    form_class = productAddForm
    success_message = "Submitted data created successfully"
    template_name = "product_add.html"
    success_url = "/productDetails"
    error_message = 'Product Name should be unique'

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class PartyUpdate(SuccessMessageMixin, UpdateView):
    model = PartyDetails
    form_class = updateParty
    success_url = "/partyDetails"
    template_name = 'Party_edit.html'


class ProductUpdate(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = productAddForm
    success_url = "/productDetails"
    template_name = "Product_edit.html"


class productShow(ListView):
    model = Product
    template_name = 'product_details.html'
    ordering = ['product_name']


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
            "product": Product.objects.all().order_by("product_name"),
            "partyInformation": PartyDetails.objects.all()
        }
        return context


class invoiceUpdate(SuccessMessageMixin, UpdateView):
    context_object_name = "data"
    template_name = 'bill-update.html'

    def get_queryset(self):
        context = {
            "product": Product.objects.all().order_by("product_name"),
            "partyInformation": PartyDetails.objects.all()
        }
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(invoiceUpdate, self).get_context_data(**kwargs)
    #     context


def gstDetails(request, pk):
    party = PartyDetails.objects.filter(id=pk)
    return JsonResponse({"party": list(party.values())})


def ProductOne(request, pk):
    products = Product.objects.filter(id=pk)
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
            Productids = [int(i)
                          for i in inputData.getlist("ProductName[]", "0")]
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
    queryset = BillDetails.objects.all().values('id', 'party__party_name', 'gst_without', 'total_amount', 'invoice_no',
                                                'date').order_by('-id')
    template_name = 'InvoiceSelect.html'


class PartyWiseProfit(ListView):
    model = BillDetails
    template_name = 'Party-wise-profit.html'


def invoiceSearchNo(request, pk):
    data = list(BillDetails.objects.filter(invoice_no=pk).values())
    return JsonResponse({"party": data})


def invoiceSearchByDate(request, start, end):
    data = list(
        BillDetails.objects.filter(date__range=[start, end]).values('party__party_name', 'gst_without', 'total_amount',
                                                                    'invoice_no',
                                                                    'date'))
    print(data)
    return JsonResponse({"party": data})


def searchByParty(request, start, end):
    data = BillDetails.objects.values('party').filter(date__range=[start, end]). \
        annotate(count=Sum('gst_without')).order_by('-count'). \
        values('party__party_name', 'party__gst_no', 'count')
    return JsonResponse({"party": list(data)})
