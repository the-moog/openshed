from django.urls import path

from . import views

urlpatterns = [
    # Item types
    path('types', views.types_listing),
    path('types/<int:type_id>', views.type_detail),
    path('types/add', views.type_add),
    path('types/<int:id>/edit', views.type_edit),
    path('types/<int:id>/delete', views.type_delete),

    # Items
    path('items', views.items_listing),
    path('items/<int:item_id>', views.item_detail),
    path('items/add', views.item_add),
    path('items/<int:id>/edit', views.item_edit),
    path('items/<int:id>/delete', views.item_delete),
    #path('<int:member_id>', views.detail),
    #path('search/', views.search),
]
