# OpenShed
OpenShed is a Django application to manage inventory. It has been developed to manage equipments for a association but it should be suitable for small business.

Openshed organizes items per types and categories. It keeps trace of who borrows the equipement.

## Installation

### Get the source
(assumes your user can create files in /opt)
```bash
cd /opt
git clone https://github.com/BegBlev/openshed
```

### Create a postgres database
```bash
sudo apt-get install postgresql
sudo su postgres
psql
```
```sql
CREATE DATABASE equipment;
CREATE USER equipment WITH PASSWORD 'secretpass';
ALTER ROLE equipment SET client_encoding TO 'utf8';
ALTER ROLE equipment SET default_transaction_isolation TO 'read committed';
ALTER ROLE equipment SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE equipment TO equipment;

\q
exit
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
