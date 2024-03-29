
"""
Vendors views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import Product, Item, Vendor
from items.forms import VendorForm
from items.utils import get_user_from_request


@login_required
def vendors_listing(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'items/vendors.html', context)


@login_required
def vendor_detail(request, id):
    vendor = Vendor.objects.get(pk=id)
    product_count = Product.objects.filter(vendor=id).count()
    item_count = Item.objects.select_related('product').filter(product__vendor=id).count()

    context = {
        'vendor': vendor,
        'product_count': product_count,
        'item_count': item_count,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'items/vendor.html', context)


@login_required
def vendor_add(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)

        if form.is_valid():
            vendor = Vendor()

            vendor.name = form.cleaned_data['name']

            vendor.save()

            return redirect(f'/items/vendors/{vendor.id}')

    else:
        form = VendorForm()

    return render(request, 'items/vendor-edit.html', {'form': form})


@login_required
def vendor_edit(request, id):
    vendor = Vendor.objects.get(pk=id)

    if request.method == 'POST':
        form = VendorForm(request.POST)

        if form.is_valid():
            vendor.name = form.cleaned_data['name']

            vendor.save()

            return redirect(f'/items/vendors/{vendor.id}')

    else:
        form = VendorForm(initial={'name': vendor.name})

    return render(request, 'items/vendor-edit.html', {'form': form, 'obj': vendor})


@login_required
def vendor_delete(request, id):
    if request.method == 'POST':
        Vendor.objects.get(pk=id).delete()

        return redirect('/items/vendors')

    return render(request, 'items/vendor-delete.html')


