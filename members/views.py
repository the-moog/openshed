from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Member
from .forms import MemberForm

from items.models import Item

# Create your views here.

@login_required
def members_listing(request):
    members = Member.objects.all().order_by('last_name', 'first_name')
    formatted_members = ["<li>{} {}</li>".format(member.last_name, member.first_name) for member in members]
    message = """<ul>{}</ul>""".format("\n".join(formatted_members))

    context = {
        'members': members
    }

    return render(request, 'members/members.html', context)

@login_required
def detail(request, member_id):
    member = Member.objects.get(pk=member_id)
    item_count = Item.objects.filter(member=member_id).count()

    context = {
        'member': member,
        'item_count': item_count
    }

    return render(request, 'members/member.html', context)

@login_required
def member_add(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)

        if form.is_valid():
            member = Member()

            member.first_name = form.cleaned_data['first_name']
            member.last_name = form.cleaned_data['last_name']

            member.save()

            return redirect(f'/members/members/{member.id}')

    else:
        form = MemberForm()

    return render(request, 'members/member-edit.html', {'form': form})

@login_required
def member_edit(request, id):
    member = Member.objects.get(pk=id)

    if request.method == 'POST':
        form = MemberForm(request.POST)

        if form.is_valid():
            member.first_name = form.cleaned_data['first_name']
            member.last_name = form.cleaned_data['last_name']

            member.save()

            return redirect(f'/members/members/{member.id}')

    else:
        form = MemberForm(initial={'first_name': member.first_name,
                                   'last_name': member.last_name})

    return render(request, 'members/member-edit.html', {'form': form})

@login_required
def member_delete(request, id):
    if request.method == 'POST':
        Member.objects.get(pk=id).delete()

        return redirect('/members/members')

    return render(request, 'members/member-delete.html')

@login_required
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
