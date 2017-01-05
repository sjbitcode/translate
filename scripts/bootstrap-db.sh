#!/bin/bash

echo "Bootstrapping postgres database..."

DB_NAME="translatedb"
DB_USER="translatedbuser"
USER_PSWD="translatedb"

sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"

sudo -u postgres psql -c "DROP USER IF EXISTS $DB_USER;"

sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$USER_PSWD';"

sudo -u postgres psql -c "ALTER ROLE $DB_USER WITH SUPERUSER;"

sudo -u postgres psql -c "CREATE DATABASE $DB_NAME WITH OWNER $DB_USER;"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"


# Edit this file, line 90, change 'peer' to 'trust'
# to allow login without password
# sudo vi /etc/postgresql/9.3/main/pg_hba.conf

# Restart postgres
# sudo /etc/init.d/postgresql restart
# sudo service postgresql restart