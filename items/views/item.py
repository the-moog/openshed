""" Item views """


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from items.models import Item
from items.forms import ItemForm
from cart.cart import Cart
from items.utils import get_user_from_request
from django.http import JsonResponse
from django.core import serializers


import logging

logger = logging.getLogger(__name__)


@login_required
def items_listing(request):
    items = Item.objects.select_related('product')  #.select_related('member')

    if request.GET.get('vendor') is not None:
        items = items.filter(product__vendor=request.GET.get('vendor'))

    if request.GET.get('supplier') is not None:
        items = items.filter(product__vendor=request.GET.get('supplier'))

    if request.GET.get('category') is not None:
        items = items.filter(product__category=request.GET.get('category'))

    if request.GET.get('product') is not None:
        items = items.filter(product=request.GET.get('product'))

    if request.GET.get('decommissioned', 'false') == 'true':
        items = items.exclude(decommissioning_date=None)
    else:
        items = items.filter(decommissioning_date=None)

    context = {
        'items': items,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    #if loan_view:
    #    page = redirect("/items/items", loan_view=loan_view)
    #else:
    page = render(request, 'items/items.html', context)
    return page


@login_required
def item_detail(request, item_id):
    item = Item.objects.get(pk=item_id)

    context = {
        'item': item,
        'is_manager': get_user_from_request(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
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
            item.product = form.cleaned_data['product']
            item.supplier = form.cleaned_data['supplier']
            item.serial = form.cleaned_data['serial']
            item.size = form.cleaned_data['size']
            item.commissioning_date = form.cleaned_data['commissioning_date']
            item.comment = form.cleaned_data['comment']
            item.image = form.cleaned_data['image']

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
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item.item = form.cleaned_data['name']
            item.product = form.cleaned_data['product']
            item.supplier = form.cleaned_data['supplier']
            item.serial = form.cleaned_data['serial']
            item.size = form.cleaned_data['size']
            item.commissioning_date = form.cleaned_data['commissioning_date']
            item.decommissioning_date = form.cleaned_data['decommissioning_date']
            item.comment = form.cleaned_data['comment']
            #handle_uploaded_file(request.FILES['image'])
            item.image = form.cleaned_data['image']

            item.save()

            return redirect(f'/items/items/{item.id}')

    else:
        form = ItemForm(initial={'name': item.item,
                                 'product': item.product,
                                 'supplier': item.supplier,
                                 'serial': item.serial,
                                 'size': item.size,
                                 'commissioning_date': item.commissioning_date,
                                 'decommissioning_date': item.decommissioning_date,
                                 'comment': item.comment,
                                 'image': item.image
                                 })

    return render(request, 'items/item-edit.html', {'form': form, 'obj': item})


@login_required
def item_delete(request, id):
    if request.method == 'POST':
        Item.objects.get(pk=id).delete()

        return redirect(f'/items/items')

    return render(request, 'items/item-delete.html')


@login_required
def cart_add(request, product_id):
    item = Item.objects.get(id=product_id)
    cart = Cart(request)
    #cart.add(item, item.unit_price, 1)
    # TODO: implement pricing
    cart.add(item, 1.23, 1)


@login_required
def cart_del(request, product_id):
    item = Item.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(item)


@login_required
def cart_detail(request):
    return render(request, 'cart.html', {'cart': Cart(request)})


@login_required
def get_reserved(request):
    user = get_user_from_request(request)
    try:
        items = Item.objects.filter(reserved_by=user.id)
    except Item.DoesNotExist:
        items = []

    for item in items:
        if item.reserved_session != request.session.session_key:
            item.reserved_session = request.session.session_key
            item.save()
            item.refresh_from_db()

    items_json = serializers.serialize('json', items)

    return JsonResponse({'reserved_count': items.count(), 'reserved_items': items_json})

