from django.urls import path

from . import views

urlpatterns = [
    # Members
    path('loans', views.loans),
    path('items', views.loanable_items),
    path('loan/<int:lending_id>', views.loan_detail),
    path('loan/<int:lending_id>/confirm', views.loan_confirm),
    path('reserve', views.loan_reserve),
    path('borrow', views.loan_complete)
    #path('lending/loan', views.lend_items),
    #path('lending/return', views.return_items)
]
