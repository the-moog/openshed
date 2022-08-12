

MP := ./manage.py

# MM = manage.py makemigrations
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
	$(MM) service_history
	$(MP) migrate
	$(MP) createsuperuser --username admin --no-input --email nobody@nowhere.com
	./djangoadmin.exp
	@echo "Creating dummy data...."
	$(MP) shell -c 'exec(open("utilities/populate_dummy_data.py").read())'
	@echo "...completed"
	$(MP) collectstatic

.PHONY: db
db:	clean
	$(PG) -c 'create database equipment;'
	$(PG) -c 'GRANT ALL PRIVILEGES ON DATABASE equipment TO equipment;'

.PHONY: clean
clean:
	-find . -type d -name migrations -exec rm -rf {} \;
	$(PG) -c 'drop database if exists equipment;'
