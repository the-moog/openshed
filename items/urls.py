from django.urls import path
from items.views import product, vendor, category, supplier, item

urlpatterns = [
    # Categories
    path('categories', category.categories_listing),
    path('categories/<int:id>', category.category_detail),
    path('categories/add', category.category_add),
    path('categories/<int:id>/edit', category.category_edit),
    path('categories/<int:id>/delete', category.category_delete),

    # Products
    path('products', product.products_listing),
    path('products/<int:product_id>', product.product_detail),
    path('products/add', product.product_add),
    path('products/<int:id>/edit', product.product_edit),
    path('products/<int:id>/delete', product.product_delete),

    # Items
    path('items', item.items_listing, name="index"),
    path('items/<int:item_id>', item.item_detail),
    path('items/add', item.item_add),
    path('items/<int:id>/edit', item.item_edit),
    path('items/<int:id>/delete', item.item_delete),
    path('items/<int:id>/cart_add', item.cart_add, name='cart_add'),
    path('items/reserved', item.get_reserved),
#    path('items/<int:id>/cart_del', item.cart_del, name='cart_clear'),
#    path('cart/item_increment/<int:id>/',
#         item.item_increment, name='item_increment'),
#    path('cart/item_decrement/<int:id>/',
#         item.item_decrement, name='item_decrement'),
#    path('cart/cart_clear/', item.cart_clear, name='cart_clear'),
    path('cart/cart_detail/', item.cart_detail, name='cart_detail'),
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
