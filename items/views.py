from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ItemType, Item, Vendor, Category
from .forms import TypeForm, ItemForm, VendorForm, CategoryForm

# Create your views here.
@login_required
def types_listing(request):
    item_types = ItemType.objects.all()

    if request.GET.get('category') != None:
        item_types = item_types.filter(category=request.GET.get('category'))

    if request.GET.get('vendor') != None:
        item_types = item_types.filter(vendor=request.GET.get('vendor'))

    context = {
        'item_types': item_types
    }

    return render(request, 'items/types.html', context)

@login_required
def type_detail(request, type_id):
    type = ItemType.objects.get(pk=type_id)
    item_count = Item.objects.filter(item_type=type).count()

    context = {
        'type': type,
        'item_count': item_count
    }

    return render(request, 'items/type.html', context)

@login_required
def type_add(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)

        if form.is_valid():
            type = ItemType()

            type.category = form.cleaned_data['category']
            type.vendor = form.cleaned_data['vendor']
            type.type = form.cleaned_data['type']
            type.description = form.cleaned_data['description']

            type.save()

            return redirect(f'/items/types/{type.id}')

    else:
        form = TypeForm()

    return render(request, 'items/type-edit.html', {'form': form})

@login_required
def type_edit(request, id):
    type = ItemType.objects.get(pk=id)

    if request.method == 'POST':
        form = TypeForm(request.POST)

        if form.is_valid():
            type.category = form.cleaned_data['category']
            type.vendor = form.cleaned_data['vendor']
            type.type = form.cleaned_data['type']
            type.description = form.cleaned_data['description']

            type.save()

            return redirect(f'/items/types/{type.id}')

    else:
        form = TypeForm(initial={'category': type.category,
                                 'vendor': type.vendor,
                                 'type': type.type,
                                 'description': type.description})

    return render(request, 'items/type-edit.html', {'form': form, 'obj': type})

@login_required
def type_delete(request, id):
    if request.method == 'POST':
        ItemType.objects.get(pk=id).delete()

        return redirect('/items/types')

    return render(request, 'items/type-delete.html')

@login_required
def items_listing(request):
    items = Item.objects.select_related('item_type').select_related('member')

    if request.GET.get('vendor') != None:
        items = items.filter(item_type__vendor=request.GET.get('vendor'))

    if request.GET.get('category') != None:
        items = items.filter(item_type__category=request.GET.get('category'))

    if request.GET.get('type') != None:
        items = items.filter(item_type=request.GET.get('type'))

    if request.GET.get('member') != None:
        items = items.filter(member=request.GET.get('member'))

    if request.GET.get('decommissioned', 'false') == 'true':
        items = items.exclude(decommissioning_date=None)
    else:
        items = items.filter(decommissioning_date=None)

    context = {
        'items': items
    }

    return render(request, 'items/items.html', context)

@login_required
def item_detail(request, item_id):
    item = Item.objects.get(pk=item_id)

    context = {
        'item': item
    }

    return render(request, 'items/item.html', context)

@login_required
def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item = Item()

            item.item = form.cleaned_data['name']
            item.item_type = form.cleaned_data['type']
            item.member = form.cleaned_data['member']
            item.serial = form.cleaned_data['serial']
            item.size = form.cleaned_data['size']
            item.commissioning_date = form.cleaned_data['commissioning_date']
            item.comment = form.cleaned_data['comment']

            item.save()

            return redirect(f'/items/items/{item.id}')

    else:
        form = ItemForm()

    return render(request, 'items/item-edit.html', {'form': form})

@login_required
def item_edit(request, id):
    item = Item.objects.get(pk=id)

    if request.method == 'POST':
        form = ItemForm(request.POST)

        if form.is_valid():
            item.item = form.cleaned_data['name']
            item.item_type = form.cleaned_data['type']
            item.member = form.cleaned_data['member']
            item.serial = form.cleaned_data['serial']
            item.size = form.cleaned_data['size']
            item.commissioning_date = form.cleaned_data['commissioning_date']
            item.decommissioning_date = form.cleaned_data['decommissioning_date']
            item.comment = form.cleaned_data['comment']

            item.save()

            return redirect(f'/items/items/{item.id}')

    else:
        form = ItemForm(initial={'name': item.item,
                                 'type': item.item_type,
                                 'serial': item.serial,
                                 'size': item.size,
                                 'commissioning_date': item.commissioning_date,
                                 'decommissioning_date': item.decommissioning_date,
                                 'comment': item.comment,
                                 'member': item.member})

    return render(request, 'items/item-edit.html', {'form': form, 'obj': item})

@login_required
def item_delete(request, id):
    if request.method == 'POST':
        Item.objects.get(pk=id).delete()

        return redirect(f'/items/items')

    return render(request, 'items/item-delete.html')

"""
Vendors views.
"""

@login_required
def vendors_listing(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors
    }

    return render(request, 'items/vendors.html', context)

@login_required
def vendor_detail(request, id):
    vendor = Vendor.objects.get(pk=id)
    type_count = ItemType.objects.filter(vendor=id).count()
    item_count = Item.objects.select_related('item_type').filter(item_type__vendor=id).count()

    context = {
        'vendor': vendor,
        'type_count': type_count,
        'item_count': item_count
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

"""
Categories views.
"""

@login_required
def categories_listing(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'items/categories.html', context)

@login_required
def category_detail(request, id):
    category = Category.objects.get(pk=id)
    item_type_count = ItemType.objects.filter(category=id).count()
    item_count = Item.objects.select_related('item_type').filter(item_type__category=id).count()

    context = {
        'category': category,
        'item_type_count': item_type_count,
        'item_count': item_count
    }

    return render(request, 'items/category.html', context)

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = Category()

            category.name = form.cleaned_data['name']

            category.save()

            return redirect(f'/items/categories/{category.id}')

    else:
        form = CategoryForm()

    return render(request, 'items/category-edit.html', {'form': form})

@login_required
def category_edit(request, id):
    category = Category.objects.get(pk=id)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            category.name = form.cleaned_data['name']

            category.save()

            return redirect(f'/items/categories/{category.id}')

    else:
        form = CategoryForm(initial={'name': category.name})

    return render(request, 'items/category-edit.html', {'form': form, 'obj': category})

@login_required
def category_delete(request, id):
    if request.method == 'POST':
        Category.objects.get(pk=id).delete()

        return redirect('/items/categories')

    return render(request, 'items/category-delete.html')
