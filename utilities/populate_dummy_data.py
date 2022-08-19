import urllib.error

from items.models import Category
from items.models import Vendor
from items.models import Supplier
from items.models import Product
from items.models import Item
from lending.models import Lending
from django.contrib.auth.models import Group, Permission
from members.models import Member
from django.contrib.contenttypes.models import ContentType
import random
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from pathlib import Path
import glob

ct_lending = ContentType.objects.get_for_model(Lending)
can_lend_group, _ = Group.objects.get_or_create(name='CanLend')
permission = Permission.objects.create(codename='CanLend',
                                       name='Can Sign Off Loans',
                                       content_type=ct_lending)
can_lend_group.permissions.add(permission)

ct = ContentType.objects.get_for_model(Item)
manager_group, _ = Group.objects.get_or_create(name='EquipmentManager')
permission = Permission.objects.create(codename='CanManageEquipment',
                                       name='Can Manage Equipment', content_type=ct)
manager_group.permissions.add(permission)

admin_user = Member.objects.get(id=1)
admin_user.groups.add(can_lend_group)
admin_user.groups.add(manager_group)

categories = ["BCD", "Regulator"]

joe_blogs = Member(first_name="Joe", last_name="Blogs")
joe_blogs.set_password("1234")
joe_blogs.email = "joseph.blogs@joesblogs.com"
joe_blogs.username = "joe"
joe_blogs.save()

USE_URLLIB = True
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

images = set(glob.glob("temp_media/image*.jpg"))
for item in range(1, NUM_ITEMS+1):
    supplier = Supplier.objects.get(id=random.randint(1, NUM_SUPPLIERS))
    product = Product.objects.get(id=random.randint(1, NUM_PRODUCTS))
    i = Item(item=f"Item {item}", product=product, supplier=supplier, serial=str(item)*4, size=str(item*10))
    img_temp = NamedTemporaryFile(delete=True)
    if USE_URLLIB:
        try:
            url = urlopen("https://picsum.photos/200/300")
            img = url.read()
        except urllib.error.URLError:
            print("URLLIB Error, using backup files")
            USE_URLLIB = False
        else:
            img_temp.write(urlopen("https://picsum.photos/200/300").read())
            img_temp.flush()
    if not USE_URLLIB:
        fp = Path(images.pop())
        print(f"Using {fp}")
        img_temp = fp.open("rb")
    img_temp.seek(0)
    i.image.save(f"image_{item}.jpg", File(img_temp), save=True)
    i.save()





