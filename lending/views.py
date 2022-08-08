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
from openshed.jsignature.utils import draw_signature

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

            # Less than one day loans are meaningless
            dt_ok = dt >= datetime.date.today()

            dt = datetime.datetime(dt.year, dt.month, dt.day, 23, 59, 59)

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
                    loan_item.item = item
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
    user = get_user_from_request(request)
    items = Item.objects.filter(Q(reserved_by__isnull=True) | Q(reserved_by__id=user.id)).select_related('product').order_by('product__category', 'id')


    # Include items that are either not reserved at all or reserved by user
    #items = items.filter(Q(reserved_by__isnull=True) | Q(reserved_by__id=user.id))

    # Exclude items that are already on loan
    lent_items = LentItems.objects.filter(return_dt__isnull=True).values_list('item')
    if len(lent_items):
        items = items.exclude(item__in=lent_items)

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


#@permission_required("CanLend")
@login_required
def loan_confirm(request, lending_id):
    loan = Lending.objects.get(pk=lending_id)
    items = LentItems.objects.filter(loan=loan)
    context = {
        'lent_to': loan.lent_to,
        'until_dt': loan.until_dt,
        'reason': loan.reason,
        'lending_id': loan.id,
        'lender': get_user_from_request(request),
        'items': [i.item for i in items]
    }
    if request.method == 'POST':
        form = LoanSignOffForm(request.POST)
        if form.is_valid():
            assert lending_id == loan.id
            loan.reason = form.cleaned_data['reason']
            loan.until_dt = form.cleaned_data['until_dt']
            loan.out_dt = datetime.datetime.utcnow()
            signature = form.cleaned_data.get('signature')
            loan.signature = draw_signature(signature, as_file=True)
            loan.lent_by = get_user_from_request(request)
            loan.save()
            logger.info("Form complete")
            return loans(request)
        else:
            logger.error("Form invalid")
    else:
        logger.info("New form")
        form = LoanSignOffForm(initial=context)

    return render(request, 'loan_confirm.html', {'form': form, 'context': context})

