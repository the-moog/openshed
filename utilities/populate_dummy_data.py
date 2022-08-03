
from items.models import Category
from items.models import Vendor
from items.models import Supplier
from items.models import Product
from items.models import Item
import random

categories = ["BCD", "Regulator"]


NUM_CATEGORIES = 10
NUM_VENDORS = 10
NUM_SUPPLIERS = 20
NUM_PRODUCTS = 50
NUM_ITEMS = 200

for category in range(1, NUM_CATEGORIES+1):
    c = Category(name=category)
    c.save()

for vendor in range(1, NUM_VENDORS+1):
    v = Vendor(name=f"Vendor {vendor}")
    v.save()

for supplier in range(1, NUM_SUPPLIERS+1):
    s = Supplier(name=f"Supplier {supplier}", contact=f"Contact {supplier}")
    s.save()

for product in range(1, NUM_PRODUCTS+1):
    vendor = Vendor.objects.get(id=random.randint(1, NUM_VENDORS))
    category = Category.objects.get(id=random.randint(1, NUM_CATEGORIES))
    p = Product(vendor=vendor, category=category, name=f"Product {product}", description=f"A long description of the product with the name {product}")
    p.save()

for item in range(1, NUM_ITEMS+1):
    supplier = Supplier.objects.get(id=random.randint(1, NUM_SUPPLIERS))
    product = Product.objects.get(id=random.randint(1, NUM_PRODUCTS))
    i = Item(item=f"Item {item}", product=product, supplier=supplier, serial=str(item)*4, size=str(item*10))
    i.save()
