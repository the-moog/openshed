from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lending
from items.models import Item
from members.models import Member
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
import json
import datetime

import logging

logger = logging.getLogger(__name__)

@login_required
def loans(request):
    loans = Lending.objects.all()
    #formatted = [f"<li>{loan.loan.item} {loan.lent_to}</li>" for loan in loans]
    #message = """<ul>{}</ul>""".format("\n".join(formatted))
    context = {
        'loans': loans
    }

    return render(request, 'loans.html', context)


@login_required
def reserve(request):

    if request.method == 'POST':
        state = request.POST['reserve_state'] == 'true'
        item = request.POST['reserve_item']
        users = Member.objects.filter(username=request.user)

        if len(users) != 1:
            return HttpResponseNotAllowed()

        items = Item.objects.filter(pk=item)

        if len(items) != 1:
            return HttpResponseBadRequest()
        user = users[0]
        item = items[0]
        reserved = False

        logging.debug(f"{state} {item} {user}")

        # Release a reserved item if timed out
        if item.reserved and datetime.datetime.utcnow() > item.reserved_until:
            item.reserved_until = None
            item.reserved_by = None
            item.save()
            item.refresh_from_db()

        if state:
            # Request to reserve
            if not item.reserved:
                item.reserved_until = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                item.reserved_by = user
                item.save()
                reserved = True
        else:
            # Request to release
            if item.reserved and item.reserved_by != user:
                reserved = True
            else:
                item.reserved_until = None
                item.reserved_by = None
                item.save()

        return HttpResponse(json.dumps({'success': reserved}), content_type="application/json")
    return HttpResponseBadRequest()


@login_required
def loan_items(request):
    items = Item.objects.select_related('product')

    users = Member.objects.filter(username=request.user)
    if len(users) != 1:
        return HttpResponseNotAllowed()
    user = users[0]

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
        'user': user
    }

    page = render(request, 'items.html', context)
    return page

@login_required
def detail(request, loan_id):
    loan = Lending.objects.get(pk=loan_id)
    item_count = Item.objects.filter(item=loan.loan.item, decommissioning_date=None).count()

    context = {
        'member': loan,
        'item_count': item_count,
        'loan_button': "btn_loan"
    }

    return render(request, 'loan.html', context)


@login_required
def loan_add(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)

        if form.is_valid():
            member = Member()

            member.first_name = form.cleaned_data['first_name']
            member.last_name = form.cleaned_data['last_name']

            member.save()

            return redirect(f'/members/members/{member.id}')

    else:
        form = MemberForm()

    return render(request, 'members/member-edit.html', {'form': form})

