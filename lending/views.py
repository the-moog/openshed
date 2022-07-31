from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Lending



@login_required
def on_hire(request):
    hires = Lending.objects.all()
    formatted = [f"<li>{hire.loan.item} {hire.lent_to}</li>" for hire in hires]
    message = """<ul>{}</ul>""".format("\n".join(formatted))
    context = {
        'hires': hires
    }

    return render(request, 'lending/loans.html', context)

