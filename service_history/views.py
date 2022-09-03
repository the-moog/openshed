from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from service_history.models import ServiceHistory, ServiceSchedule
from service_history.forms import ServiceScheduleForm
from django.contrib.auth import get_user
from items.models.item import Item
import re
from schedule.models import Rule as RRule
from dateutil import rrule


@login_required
def schedule_listing(request):
    schedules = ServiceSchedule.objects.all()

    context = {
        'schedules': schedules,
        'is_manager': get_user(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'schedules.html', context)


@login_required
def schedule_detail(request, id):
    schedule = ServiceSchedule.objects.get(pk=id)
    item_count = Item.objects.filter(schedule=schedule).count()

    context = {
        'schedule': schedule,
        'item_count': item_count,
        'is_manager': get_user(request).groups.filter(name__in=['EquipmentManager', "Admin"]).exists()
    }

    return render(request, 'schedule.html', context)


rrule_types = {
    'y': rrule.YEARLY,
    'm': rrule.MONTHLY,
    'w': rrule.WEEKLY,
    'd': rrule.DAILY
}

@login_required
def schedule_add(request):
    if request.method == 'POST':
        form = ServiceScheduleForm(request.POST)

        if form.is_valid():
            schedule = ServiceSchedule()

            interval_type = form.cleaned_data['interval_type']
            interval = form.cleaned_data['interval']

            # ret = {u: None for u in 'dwmy'}
            # if interval_type == 'o':
            #     for unit in 'dwmy':
            #         if unit in interval:
            #             res = re.search(f"(\[0-9]+){unit}", interval)
            #             if not res:
            #                 raise ValueError("How to handle this?")
            #             ret[unit] = res.groups[0][1]
            # else:
            #     ret[interval_type] = int(interval)

            category = form.cleaned_data['category']
            rules = RRule.objects.filter(serviceschedule__category=category).count()
            rule = RRule(name=f"Category-{category}-{rules+1}", description=form.cleaned_data['comment'],
                         frequency=rrule_types[interval_type], params=f"interval:{interval}")
            rule.save()

            schedule.interval = rule
            schedule.category = form.cleaned_data['category']

            schedule.save()

            return schedule_listing(request)

    else:
        DEFAULT = 1
        form = ServiceScheduleForm(initial={'interval_type': 'y',
                                            'interval': DEFAULT,
                                            "comment": f"Service every {DEFAULT} year(s)"})

    return render(request, 'schedule-edit.html', {'form': form})


@login_required
def schedule_edit(request, id):
    schedule = ServiceSchedule.objects.get(pk=id)

    if request.method == 'POST':
        form = ServiceScheduleForm(request.POST)

        if form.is_valid():
            schedule.interval = form.cleaned_data['interval']
            schedule.comment = form.cleaned_data['comment']
            schedule.category = form.cleaned_data['category']

            schedule.save()

            return redirect(f'service_schedule/{schedule.id}')

    else:
        form = ServiceScheduleForm(initial={'interval': schedule.interval,
                                            'comment': schedule.comment,
                                            'category': schedule.category,
                                            })

    return render(request, 'items/product-edit.html', {'form': form, 'obj': schedule})


@login_required
def schedule_delete(request, id):
    if request.method == 'POST':
        ServiceSchedule.objects.get(pk=id).delete()

        return redirect('schedules.html')

    return render(request, 'schedule-delete.html')

