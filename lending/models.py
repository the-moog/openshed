from django.db import models
from items.models import Item
from members.models import Member


# Item loans model
class Lending(models.Model):
    lent_by = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='lb', null=True, default=None)
    lent_to = models.ForeignKey(Member, on_delete=models.PROTECT, related_name='lt')
    out_dt = models.DateTimeField(default=None, null=True)
    until_dt = models.DateField(blank=False)
    billed = models.DecimalField(max_digits=6, decimal_places=2, default=None, null=True)
    reason = models.TextField(blank=False)
    signature = models.ImageField(default=None, null=True, upload_to="signatures")

    @property
    def active(self):
        return self.out_dt is not None and self.billed is None

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

    def __str__(self):
        return self.lent_to.display_name() + ": " + str(self.signature)


# List of items within the loan
class LentItems(models.Model):
    loan = models.ForeignKey(Lending, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    return_dt = models.DateField(default=None, null=True)
    returned_by = models.ForeignKey(Member, on_delete=models.PROTECT, null=True, default=None)


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

