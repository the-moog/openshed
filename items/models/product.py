from django.db import models


# Products
class Product(models.Model):
    """Products are made by Vendors and sold by Suppliers"""
    vendor = models.ForeignKey('Vendor', null=True, on_delete=models.PROTECT)
    category = models.ForeignKey('Category', null=True, on_delete=models.PROTECT)

    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.long_name()

    def long_name(self):
        return f"({self.category.name}) {self.name} {self.description} by {self.vendor.name}"

