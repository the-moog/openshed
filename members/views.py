from django.shortcuts import render
from django.db.models import Q

from .models import Member

# Create your views here.

def listing(request):
    members = Member.objects.all().order_by('last_name', 'first_name')
    formatted_members = ["<li>{} {}</li>".format(member.last_name, member.first_name) for member in members]
    message = """<ul>{}</ul>""".format("\n".join(formatted_members))

    context = {
        'members': members
    }

    return render(request, 'members/members.html', context)

def detail(request, member_id):
    member = Member.objects.get(pk=member_id)
    message = f"Nom: {member.last_name} Prénom: {member.first_name}"

    return HttpResponse(message)

def search(request):
    query = request.GET.get('query')

    if not query:
        members = Member.objects.all()
    else:
        members = Member.objects.filter(Q(last_name__icontains=query) | Q(first_name__icontains=query))

        if not members.exists():
            message = f"Not found {query}"
        else:
            formatted_members = ["<li>{} {}</li>".format(member.last_name, member.first_name) for member in members]
            message = """<ul>{}</ul>""".format("\n".join(formatted_members))

    return HttpResponse(message)
