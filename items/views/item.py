""" Item views """


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import ItemType, Item
from items.forms import TypeForm, ItemForm

import logging

logger = logging.getLogger(__name__)




@login_required
def items_listing(request):
    items = Item.objects.select_related('item_type')  #.select_related('member')

    if request.GET.get('vendor') != None:
        items = items.filter(item_type__vendor=request.GET.get('vendor'))

    if request.GET.get('category') != None:
        items = items.filter(item_type__category=request.GET.get('category'))

    if request.GET.get('type') != None:
        items = items.filter(item_type=request.GET.get('type'))

    #if request.GET.get('member') != None:
        #items = items.filter(member=request.GET.get('member'))

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
    logger.debug("item_add")
    if request.method == 'POST':
        form = ItemForm(request.POST)
        logger.debug("POST")
        if form.is_valid():
            logger.debug("Adding")
            item = Item()

            item.item = form.cleaned_data['name']
            item.item_type = form.cleaned_data['type']
            #item.member = form.cleaned_data['member']
            item.serial = form.cleaned_data['serial']
            item.size = form.cleaned_data['size']
            item.commissioning_date = form.cleaned_data['commissioning_date']
            item.comment = form.cleaned_data['comment']

            item.save()

            return redirect(f'/items/items/{item.id}')
        else:
            logger.debug("Form not valid")

    else:
        logger.debug(f"{request}")
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
            #item.member = form.cleaned_data['member']
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
                                 #'member': item.member
                                 })

    return render(request, 'items/item-edit.html', {'form': form, 'obj': item})


@login_required
def item_delete(request, id):
    if request.method == 'POST':
        Item.objects.get(pk=id).delete()

        return redirect(f'/items/items')

    return render(request, 'items/item-delete.html')

