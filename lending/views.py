from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lending
from items.models import Item


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
def loan_items(request):
    items = Item.objects.select_related('product')

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

