from django.urls import path
from items.views import vendor, itemtype, category, supplier, item

urlpatterns = [
    # Categories
    path('categories', category.categories_listing),
    path('categories/<int:id>', category.category_detail),
    path('categories/add', category.category_add),
    path('categories/<int:id>/edit', category.category_edit),
    path('categories/<int:id>/delete', category.category_delete),

    # Item types
    path('types', itemtype.types_listing),
    path('types/<int:type_id>', itemtype.type_detail),
    path('types/add', itemtype.type_add),
    path('types/<int:id>/edit', itemtype.type_edit),
    path('types/<int:id>/delete', itemtype.type_delete),

    # Items
    path('items', item.items_listing),
    path('items/<int:item_id>', item.item_detail),
    path('items/add', item.item_add),
    path('items/<int:id>/edit', item.item_edit),
    path('items/<int:id>/delete', item.item_delete),
    #path('<int:member_id>', views.detail),
    #path('search/', views.search),

    # Vendors
    path('vendors', vendor.vendors_listing),
    path('vendors/<int:id>', vendor.vendor_detail),
    path('vendors/add', vendor.vendor_add),
    path('vendors/<int:id>/edit', vendor.vendor_edit),
    path('vendors/<int:id>/delete', vendor.vendor_delete),

    # Suppliers
    path('suppliers', supplier.supplier_listing),
    path('suppliers/<int:id>', supplier.supplier_detail),
    path('suppliers/add', supplier.supplier_add),
    path('suppliers/<int:id>/edit', supplier.supplier_edit),
    path('suppliers/<int:id>/delete', supplier.supplier_delete),
]
