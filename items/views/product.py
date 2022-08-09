from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import Product, Item
from items.forms import ProductForm
from items.utils import get_user_from_request


@login_required
def products_listing(request):
    products = Product.objects.all()

    if request.GET.get('category') is not None:
        products = products.filter(category=request.GET.get('category'))

    if request.GET.get('vendor') is not None:
        products = products.filter(vendor=request.GET.get('vendor'))

    context = {
        'products': products,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'items/products.html', context)


@login_required
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    item_count = Item.objects.filter(product=product).count()

    context = {
        'product': product,
        'item_count': item_count,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'items/product.html', context)


@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = Product()

            product.category = form.cleaned_data['category']
            product.vendor = form.cleaned_data['vendor']
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']

            product.save()

            return redirect(f'/items/products/{product.id}')

    else:
        form = ProductForm()

    return render(request, 'items/product-edit.html', {'form': form})


@login_required
def product_edit(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product.category = form.cleaned_data['category']
            product.vendor = form.cleaned_data['vendor']
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']

            product.save()

            return redirect(f'/items/products/{product.id}')

    else:
        form = ProductForm(initial={'category': product.category,
                                 'vendor': product.vendor,
                                 'name': product.name,
                                 'description': product.description})

    return render(request, 'items/product-edit.html', {'form': form, 'obj': product})


@login_required
def product_delete(request, id):
    if request.method == 'POST':
        Product.objects.get(pk=id).delete()

        return redirect('/items/products')

    return render(request, 'items/product-delete.html')