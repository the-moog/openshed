from django.db import models
from items.models import Item
from members.models import Member

# List of items within the loan
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
    billed = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    reason = models.TextField()

    @property
    def cost_estimate(self):
        # TODO Make a costs table
        return 1.23

    @property
    def cost(self):
        # TODO Make a costs table
        return 4.56

    @property
    def returned(self):
        return self.until_dt is not None

    @property
    def paid(self):
        return False

    @property
    def outstanding(self):
        return 2.34


# Payments against loan
class LoanPayments(models.Model):
    METHODS = [
        ("CA", "Cash"),
        ("CH", "Cheque"),
        ("OB", "Online Banking"),
        ("DC", "Debit Card"),
        ("PP", "PayPal"),
        ("BA", "BACS")
    ]
    loan = models.ForeignKey(Lending, on_delete=models.PROTECT)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2, default=None)
    paid_on = models.DateField(blank=False)
    paid_by = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='pb')
    method = models.CharField(max_length=2, choices=METHODS)
    reference = models.CharField(max_length=50, blank=True, default='')

    @property
    def total_paid(self):
        return 999
