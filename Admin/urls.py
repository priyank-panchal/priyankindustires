from unicodedata import name
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
    path('invoiceUpdate/<int:pk>', BillUpdate.as_view(), name="invoice-update"),
    path('invoice/productOne/<int:pk>', ProductOne, name='productOne'),
    path('invoice/gstNo/<int:pk>', gstDetails, name='gstNo'),
    path('invoice/allData/', allData.as_view(), name='data-all'),
    path('invoice/print/<int:pk>', invoicePrint, name='invoice-print'),
    path('invoice/invoiceNumber/', getInvoiceNumber.as_view(),
         name='get-invoicenumber'),
    path('invoice/show/', invoiceShow.as_view(), name='invoice-show'),
    path('searchByNo/<int:pk>', invoiceSearchNo, name='search-by-number'),
    path('searchByDate/<str:start>/<str:end>',
         invoiceSearchByDate, name="search-by-date"),
    path('party-wise-profit/', PartyWiseProfit.as_view(), name="partyWiseProfit"),
    path('searchByParty/<str:start>/<str:end>',
         searchByParty, name="search-by"),
    path('delete-invoice/<int:pk>',
         deleteInvoice.as_view(), name="delete-invoice"),



    # purchase-urls
    path('purchase-invoice', purchaseShow.as_view(), name="purchasemaster"),
    path('purchase-show', purchaseshowbill.as_view(), name="purchase-show"),
    path('purchaseInsert/', purchaseInsert.as_view(), name="purchase_insert"),
    path('deletePurchase/<str:pk>',
         deletePurchase.as_view(), name="deletePurchase"),
    path('editPurchase/<str:pk>', editPurchase.as_view(), name="editPurchase"),


    # credit urls
    path('credit/', creditShow.as_view(), name="credit_show"),
    path('creditInsert/<str:pk>', CreditInsert.as_view(), name="credit_insert"),
    path('deletePayment_by/<str:pk>',deletePayment_by.as_view(),name="delete_payment_by")



]
