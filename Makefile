
MP := ./manage.py
MM := $(MP) makemigrations
PASSFILE := password.env
PASS := PGPASSWORD=1234
PSQL := /usr/bin/psql
PG := $(PASS) $(PSQL) -h localhost -p 5432 -U postgres

.PHONY: all
all: db
	$(MM) items
	$(MM) members
	$(MM) lending
	$(MP) migrate
	$(MP) createsuperuser --username admin --no-input --email nobody@nowhere.com
	./djangoadmin.exp
	$(MP) shell -c 'exec(open("utilities/populate_dummy_data.py").read())'

.PHONY: db
db:
	$(PG) -c 'drop database if exists equipment;'
	$(PG) -c 'create database equipment;'
	$(PG) -c 'GRANT ALL PRIVILEGES ON DATABASE equipment TO equipment;'

