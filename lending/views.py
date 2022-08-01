from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lending
from items.models import Item
from members.models import Member
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
import json
from items.utils import reserve, get_user_from_request
from django.db.models import Q

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
def loan_items(request):
    """Return a list of items available for loan including those that are reserved by the user"""
    items = Item.objects.all().select_related('product').order_by('product__category', 'id')
    user = get_user_from_request(request)

    items = items.filter(Q(reserved_by__isnull=True) | Q(reserved_by__id=user.id))

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

