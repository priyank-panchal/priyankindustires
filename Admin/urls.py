from django.urls import path, include
from Admin.views import *

urlpatterns = [
    path('', index, name='index'),
    path('partyDetails/', partyShow.as_view(), name='part-details'),
    path('partyAdd/', partyAdd.as_view(), name='Party_Add'),
    path('partyUpdate/<int:pk>', PartyUpdate.as_view(), name="party_update"),
    path('productDetails/', productShow.as_view(), name='product-details'),
    path('productAdd/', productAdd.as_view(), name='product_add'),
    path('productUpdate/<int:pk>', ProductUpdate.as_view(), name='product_update'),
    path('invoice/', invoiceBillShow.as_view(), name='invoiceBill'),
    path('invoiceUpdate/<int:pk>', invoiceUpdate.as_view(), name="invoice-update"),
    path('invoice/productOne/<int:pk>', ProductOne, name='productOne'),
    path('invoice/gstNo/<int:pk>', gstDetails, name='gstNo'),
    path('invoice/allData/', allData.as_view(), name='data-all'),
    path('invoice/print/<int:pk>', invoicePrint, name='invoice-print'),
    path('invoice/invoiceNumber/', getInvoiceNumber.as_view(), name='invoice-print'),
    path('invoice/show/', invoiceShow.as_view(), name='invoice-show'),
    path('searchByNo/<int:pk>', invoiceSearchNo, name='search-by-number'),
    path('searchByDate/<str:start>/<str:end>',
         invoiceSearchByDate, name="search-by-date"),
    path('party-wise-profit/', PartyWiseProfit.as_view(), name="partyWiseProfit"),
    path('searchByParty/<str:start>/<str:end>', searchByParty, name="search-by")
]
