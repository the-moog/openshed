"""
Categories views.
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import Product, Item, Category
from items.forms import CategoryForm


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
    product_count = Product.objects.filter(category=id).count()
    item_count = Item.objects.select_related('product').filter(product__category=id).count()

    context = {
        'category': category,
        'product_count': product_count,
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
