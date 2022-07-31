from django.urls import path

from . import views

urlpatterns = [
    # Members
    path('lending', views.on_hire),
    #path('lending/<int:lending_id>', views.detail),
    #path('lending/loan', views.lend_items),
    #path('lending/return', views.return_items)
]
