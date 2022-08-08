"""
Supplier views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import Supplier
from items.forms import SupplierForm
from items.utils import get_user_from_request

@login_required
def supplier_listing(request):
    suppliers = Supplier.objects.all()

    context = {
        'suppliers': suppliers,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'items/suppliers.html', context)


@login_required
def supplier_detail(request, id):
    supplier = Supplier.objects.get(pk=id)
  #  product_count = Product.objects.filter(supplier=id).count()
  #  item_count = Item.objects.select_related('product').filter(product__supplier=id).count()

    context = {
        'supplier': supplier,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
        # 'type_count': product_count,
        # 'item_count': item_count
    }

    return render(request, 'items/supplier.html', context)


@login_required
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            supplier = Supplier()

            supplier.name = form.cleaned_data['name']
            supplier.contact = form.cleaned_data['contact']
            supplier.email = form.cleaned_data['email']
            supplier.phone = form.cleaned_data['phone']
            supplier.address = form.cleaned_data['address']
            supplier.url = form.cleaned_data['url']

            supplier.save()

            return redirect(f'/items/suppliers/{supplier.id}')
    else:
        form = SupplierForm()

    return render(request, 'items/supplier-edit.html', {'form': form})


@login_required
def supplier_edit(request, id):
    supplier = Supplier.objects.get(pk=id)

    if request.method == 'POST':
        form = SupplierForm(request.POST)

        if form.is_valid():
            supplier.name = form.cleaned_data['name']
            supplier.contact = form.cleaned_data['contact']
            supplier.email = form.cleaned_data['email']
            supplier.phone = form.cleaned_data['phone']
            supplier.address = form.cleaned_data['address']
            supplier.url = form.cleaned_data['url']

            supplier.save()

            return redirect(f'/items/suppliers/{supplier.id}')

    else:
        form = SupplierForm(initial={'name': supplier.name,
                                   'address': supplier.address,
                                   'contact': supplier.contact,
                                   'email': supplier.email,
                                   'phone': supplier.phone,
                                   'url': supplier.url})

    return render(request, 'items/supplier-edit.html', {'form': form, 'obj': supplier})


@login_required
def supplier_delete(request, id):
    if request.method == 'POST':
        Supplier.objects.get(pk=id).delete()

        return redirect('/items/suppliers')

    return render(request, 'items/suppliers-delete.html')


