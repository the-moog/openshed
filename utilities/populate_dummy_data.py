
from items.models import Category
from items.models import Vendor
from items.models import Supplier
from items.models import Product
from items.models import Item
from lending.models import Lending
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
import random
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

ct_lending = ContentType.objects.get_for_model(Lending)
new_group, _ = Group.objects.get_or_create(name='CanLend')
permission = Permission.objects.create(codename='CanLend',
                                       name='Can Sign Off Loans',
                                       content_type=ct_lending)
new_group.permissions.add(permission)

ct = ContentType.objects.get_for_model(Item)
new_group, _ = Group.objects.get_or_create(name='EquipmentManager')
permission = Permission.objects.create(codename='CanManageEquipment',
                                       name='Can Manage Equipment', content_type=ct)
new_group.permissions.add(permission)

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
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen("https://picsum.photos/200/300").read())
    img_temp.flush()
    img_temp.seek(0)
    i.image.save(f"image_{item}.jpg", File(img_temp), save=True)
    i.save()



