from django.urls import path, include
from Admin.views import *
urlpatterns = [
    path('index/',index , name='index'),
    path('partyDetails/',partyShow.as_view() , name = 'part-details'),
    path('partyAdd/', partyAdd.as_view(), name='Party_Add'),
    path('productDetails/',productShow.as_view(),name = 'product-details'),
    path('productAdd/',productAdd.as_view(),name ='product_add'),
    path('invoice/',invoiceBillShow.as_view(),name = 'invoiceBill'),
    path('invoice/productOne/<int:pk>',ProductOne,name='productOne'),
    path('invoice/gstNo/<int:pk>',gstDetails,name ='gstNo'),
    path('invoice/allData/',allData.as_view(),name='data-all'),
    path('invoice/print/<int:pk>',invoicePrint,name='invoice-print'),
    path('invoice/invoiceNumber/', getInvoiceNumber.as_view(), name='invoice-print')

]
