# FORK - Work in progress

This is a fork of [openshed](https://github.com/openshed-community/openshed) (new name TBD).  It is very much work in progress, though getting there.

The intention is to create a fully functional application to manage a kit store for a dive club, though it could be used for any similar equipment hire.  It will be hooked into a [Wagtail CMS](https://wagtail.org/) that forms our club website.

This is such a deviation that I don't think it's the same project any longer....

Intended features:

* Streamline and automate initial setup
* Dropping independent Member model, now based on Django's User model **(DONE)**
* Working with NFC/QR id tags **(DONE)**
* Better implementation of equipment loans, using jsignature to sign for receipts and a shopping cart like functionality **(DONE)**
* Equipment service history **(WIP)**
* Equipment sets **(PLANNED)**
* Permission levels
  * Zero - Just read a tag, for lost items to be returned (WIP)
  * User - Checkin and checkout items **(DONE)**
  * Admin - Modify records and crete new items **(DONE)**
* Equipment reservation **(DONE)**
* Item images **(DONE)**
* Billing for item hire **(PLANNED)**
* eMail notification **(PLANNED)**

***NOTE: In doing the above there are significant differences to the database schema compared to the original project, it is probably not possible to simply upgrade the database.***

# OpenShed

OpenShed is a Django application to manage inventory. It has been developed to manage equipment for a BSAC Dive Club, but it could be used by anybody that has a collection of kit that needs some sort of management.

## Installation

The following instructions have changed from the original project, still work in progress.

### Get the source

(assumes your user can create files in /opt)

```bash
cd /opt
git clone https://github.com/the-moog/openshed
```

### Create a postgres database

* Install postgres
* Create the database
* Create the admin user
* Set permissions

```bash
sudo apt-get install postgresql
cd openshed
make clean
```

### Populate with dummy data (optional)

```bash
make dummy
```

### Sensible settings

Edit <b><i>openshed/settings.py</i></b><br>
Put a secret key between the quotes

```python
SECRET_KEY = 'some secret here'
```

Set the permitted host(s)

```python
ALLOWED_HOSTS = ['localhost']
```

Connect database

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'equipment',
        'USER': 'equipment',
        'PASSWORD': 'secretpass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Set a language and timezone

```python
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
```

### Install dependencies

```bash
sudo apt-get install libpq-dev
```

### Use pipenv to prevent dependency hell

```bash
sudo pip3 install pipenv
cd /opt/openshed
pipenv install
pipenv update
```

### Prepare and run

```bash
cd /opt/openshed
pipenv shell
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

## About OpenShed

With OpenShed you can list all your equipments.
![Screenshot of items list](docs/media/items.png "Items view")

If you want to know all equipments of 1 type, just select the type and then the items.
![Screenshot of types list](docs/media/types.png "Types view")
![Screenshot of type details](docs/media/type.png "Type view")
![Screenshot of items list for 1 type](docs/media/type-items.png "Items for 1 type view")

If you want to know the list of equipment assigned to 1 person just select the member and then the equipments.
![Screenshot of members list](docs/media/members.png "Members view")
![Screenshot of member details](docs/media/member.png "Member view")
![Screenshot of items list for 1 member](docs/media/member-items.png "Items for 1 member view")

# Thanks

Openshed is largely inspired by [NetBox](https://github.com/netbox-community/netbox). I would like to thank them for the amazing work they have done.
