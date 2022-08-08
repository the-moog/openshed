from django.urls import path

from . import views
from items.views import *

urlpatterns = [
    # Members
    path('loans', views.loans),
    path('items', views.loanable_items),
    path('lending/<int:id>', views.loan_detail),
    path('loan/<int:lending_id>/confirm', views.loan_confirm),
    path('reserve', views.loan_reserve),
    path('borrow', views.loan_complete),
    path('products/<int:product_id>', product.product_detail),
    path('vendors/<int:id>', vendor.vendor_detail),
    path('suppliers/<int:id>', supplier.supplier_detail),
    path('items/<int:item_id>', item.item_detail)
    #path('lending/loan', views.lend_items),
    #path('lending/return', views.return_items)
]
