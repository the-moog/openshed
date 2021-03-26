from django.urls import path

from . import views

urlpatterns = [
    # Categories
    path('categories', views.categories_listing),
    path('categories/<int:id>', views.category_detail),
    path('categories/add', views.category_add),
    path('categories/<int:id>/edit', views.category_edit),
    path('categories/<int:id>/delete', views.category_delete),

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

    # Vendors
    path('vendors', views.vendors_listing),
    path('vendors/<int:id>', views.vendor_detail),
    path('vendors/add', views.vendor_add),
    path('vendors/<int:id>/edit', views.vendor_edit),
    path('vendors/<int:id>/delete', views.vendor_delete),
]
