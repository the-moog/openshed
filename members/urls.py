from django.urls import path

from . import views

urlpatterns = [
    # Members
    path('members', views.members_listing),
    path('members/<int:member_id>', views.detail),
    path('members/add', views.member_add),
    path('members/<int:id>/edit', views.member_edit),
    path('members/<int:id>/delete', views.member_delete),
    path('search/', views.search),
]
