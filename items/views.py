from django.shortcuts import render, redirect

from .models import ItemType, Item
from .forms import TypeForm, TypeDeleteForm

# Create your views here.
def types_listing(request):
    item_types = ItemType.objects.all()

    context = {
        'item_types': item_types
    }

    return render(request, 'items/types.html', context)

def type_detail(request, type_id):
    type = ItemType.objects.get(pk=type_id)

    context = {
        'type': type
    }

    return render(request, 'items/type.html', context)

def type_add(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)

        if form.is_valid():
            type = ItemType()

            type.vendor = form.cleaned_data['vendor']
            type.type = form.cleaned_data['type']
            type.description = form.cleaned_data['description']

            type.save()

            return redirect(f'types/{type.id}')

    else:
        form = TypeForm()

    return render(request, 'items/type-add.html', {'form': form})

def type_delete(request, id):
    if request.method == 'POST':
        form = TypeDeleteForm(request.POST)

        if form.is_valid():
            ItemType.objects.filter(pk=id).delete()

            return redirect('/items/types')

    else:
        form = TypeDeleteForm()

    return render(request, 'items/type-delete.html', {'form': form})

def items_listing(request):
    items = Item.objects.all().select_related('item_type').select_related('member')

    context = {
        'items': items
    }

    return render(request, 'items/items.html', context)

def item_detail(request, item_id):
    item = Item.objects.get(pk=item_id)

    context = {
        'item': item
    }

    return render(request, 'items/item.html', context)
