from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Lending, LentItems
from .forms import LoanOutForm, LoanSignOffForm
from items.models import Item
from members.models import Member
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
import json
from items.utils import reserve, get_user_from_request
from django.db.models import Q
import datetime
from items.utils import release_reserved

import logging

logger = logging.getLogger(__name__)


@login_required
def loans(request):
    loans = Lending.objects.all()

    context = {
        'loans': loans
    }

    return render(request, 'loans.html', context)


@login_required
def loan_complete(request):
    user = get_user_from_request(request)

    dt_ok = reason_ok = items_ok = True

    if request.method == "POST":
        form = LoanOutForm(request.POST)
        ok = form.is_valid()
        if ok:
            # Make sure the dt is not in the past
            dt = form.cleaned_data['until_dt']
            dt_ok = dt >= datetime.date.today()

            dt = datetime.datetime(dt.year, dt.day, dt.month, 23, 59, 59)

            reason = form.cleaned_data['reason']
            reason_ok = len(reason) > 20

            try:
                items = Item.objects.filter(reserved_by=user.id)
            except Item.DoesNotExist:
                items = []

            items_ok = len(items) > 0

            if dt_ok and reason_ok and items_ok:
                loan = Lending()
                loan.lent_to = user
                loan.until_dt = dt
                loan.reason = reason
                loan.save()

                for item in items:
                    loan_item = LentItems()
                    loan_item.loan = loan
                    loan_item.save()
                    loan_item.items.add(item)
                    release_reserved(item)
                    loan_item.save()

                return loans(request)
            else:
                logger.debug("Form go round")
        else:
            logger.debug("Form not valid")

    else:
        logger.debug(f"{request}")
        form = LoanOutForm()

    context = {'form': form,
               'errors': {
                   'until_dt': dt_ok,
                   'reason': reason_ok,
                   'items': items_ok
                    }
               }

    return render(request, 'loan_complete.html', context)


@login_required
def loan_reserve(request):
    if request.method == 'POST':
        item = request.POST['reserve_item']

        try:
            user = get_user_from_request(request)
        except Member.DoesNotExist:
            return HttpResponseNotAllowed()

        try:
            item = Item.objects.get(pk=item)
        except Item.DoesNotExist:
            return HttpResponseBadRequest

        logging.debug(f"{item} {user}")
        reserved = reserve(item, user, request.session)

        return HttpResponse(json.dumps({'reserved': reserved}), content_type="application/json")
    return HttpResponseBadRequest()


@login_required
def loanable_items(request):
    """Return a list of items available for loan including those that are reserved by the user"""
    items = Item.objects.all().select_related('product').order_by('product__category', 'id')
    user = get_user_from_request(request)

    # Include items that are either not reserved at all or reserved by user
    items = items.filter(Q(reserved_by__isnull=True) | Q(reserved_by__id=user.id))

    # Exclude items that are already on loan
    items = items.exclude(lentitems__items__in=items)

    context = {
        'items': items,
        'user': user
    }

    page = render(request, 'items.html', context)
    return page


@login_required
def loan_detail(request, loan_id):
    loan = Lending.objects.get(pk=loan_id)
    item_count = Item.objects.filter(item=loan.loan.item, decommissioning_date=None).count()

    context = {
        'member': loan,
        'item_count': item_count,
        'loan_button': "btn_loan"
    }

    return render(request, 'loan.html', context)


@permission_required("CanLend")
@login_required
def loan_confirm(request, lending_id):
    loan = Lending.objects.get(id=lending_id)
    context = {
        'hire_to': loan.lent_to,
        'from_dt': loan.out_dt,
        'to_date': loan.until_dt,
        'reason': loan.reason,
        'lending_id': loan.id,
        'lender': get_user_from_request(request)
    }
    if request.method == 'POST':
        form = LoanSignOffForm(request.POST)
        if form.is_valid():
            assert form.cleaned_data['lending_id'] == loan.id
            loan.reason = form.cleaned_data['reason']
            loan.until_dt = form.cleaned_data['until_dt']
            loan.out_dt = form.cleaned_data['out_dt']
            loan.lent_by = context.lender
            loan.save()

            return redirect(f'lending')
    else:
        form = LoanSignOffForm(loan_confirm)

    return render(request, 'loan_confirm.html', {'form': form, 'context': context})

