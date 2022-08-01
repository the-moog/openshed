from django.urls import path

from . import views

urlpatterns = [
    # Members
    path('loans', views.loans),
    path('items', views.loan_items),
    path('loan/<int:lending_id>', views.detail),
    path('loan/add', views.loan_add),
    path('reserve', views.reserve)
    #path('lending/loan', views.lend_items),
    #path('lending/return', views.return_items)
]
