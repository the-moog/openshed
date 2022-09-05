from schedule.models import Rule, Event, EventRelation
from django.db import models
from dateutil.relativedelta import relativedelta
import datetime


class RRule(Rule):
    # Subclass of Rule that makes any rule with the same frequency and params the same rule

    @property
    def rrule(self):
        return self.frequency + "_" + super().__str__()

    def save(self, *args, **kw):
        _existing = RRule.objects.filter(frequency=self.frequency, params=self.params)
        if _existing.count():
            existing = _existing.last()
        else:
            try:
                existing = RRule.objects.get(id=self.id)
            except RRule.DoesNotExist:
                existing = None

        if existing:
            return existing
        super().save(*args, **kw)
        return self

    def __str__(self):
        return self.rrule


class ServiceSchedule(models.Model):
    """A given Category can have zero or more service schedules"""
    rule = models.OneToOneField('service_history.RRule', on_delete=models.PROTECT)
    category = models.ForeignKey('items.Category', on_delete=models.PROTECT)
    object_hash = models.CharField(unique=True, max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rule', 'category'], name='unique service schedule')
        ]

    def save(self, *args, **kw):
        from items.models import Item
        self.object_hash = str(self)

        schedule = ServiceSchedule.objects.filter(object_hash=self.object_hash).last()
        # As we are adding or updating a Rule we need to update the calendars for Items affected
        items = Item.objects.filter(product__category=self.category)
        for item in items:
            if schedule:
                # If the rule exists, just check the Event for that rule
                events = Event.objects.filter(rule=schedule.rule, calendar=item.calendar)
                rule = schedule.rule
                event = events.last()
            else:
                event = None
                rule = self.rule.save()
                super().save(*args, **kw)

            if not event:
                # Only add events for rules that don't exist
                event = Event(start=datetime.date.today(),
                              end=datetime.date.today()+relativedelta(years=99),
                              rule=rule, calendar=item.calendar)
                event.save()
                item.calendar.events.add(event)
                EventRelation.objects.create_relation(event, item, "Service Schedule")

        super().save(*args, **kw)

    def __str__(self):
        return str(self.rule) + "_" + str(self.category_id)


class ServiceHistory(models.Model):
    """A given item of a Category that is serviceable (in that it has a ServiceSchedule)
    can have multiple service history records stored in a calendar"""
    item = models.OneToOneField('items.Item', on_delete=models.CASCADE)
    report = models.FileField()
    service_by = models.ForeignKey('items.Supplier', on_delete=models.PROTECT)
    result_is_good = models.BooleanField()







