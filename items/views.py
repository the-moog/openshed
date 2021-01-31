from django.shortcuts import render

from .models import ItemType, Item

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
