from django.db import models
from items.models import Item
from members.models import Member


class LentItems(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    return_dt = models.DateField(default=None)
    return_by = models.ForeignKey(Member, on_delete=models.PROTECT)


# Item loans model
class Lending(models.Model):
    loan = models.ForeignKey(LentItems, on_delete=models.PROTECT)
    lent_by = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='lb')
    lent_to = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='lt')
    out_dt = models.DateTimeField(blank=False)
    until_dt = models.DateField(blank=False)
    paid = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    reason = models.TextField()

    @property
    def cost_estimate(self):
        # TODO Make a costs table
        return 1.23

    @property
    def cost(self):
        # TODO Make a costs table
        return 4.56

