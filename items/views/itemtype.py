from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import ItemType, Item
from items.forms import TypeForm

@login_required
def types_listing(request):
    item_types = ItemType.objects.all()

    if request.GET.get('category') is not None:
        item_types = item_types.filter(category=request.GET.get('category'))

    if request.GET.get('vendor') is not None:
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