---
layout: default
title: Postgres Setup
nav_order: 6
---

# Postgres Setup

To get started, log in as the linux 'postgres' user (who should be set up by default when installing postgres on the system). This user has access to run psql/postgres commands. (You should make sure that a password is set up for the linux postgres account)

``` bash
$ sudo -i -u postgres
```

Log into the 'psql' interface:

``` bash
$ psql
```

List all current databases:

``` bash
postgres=# \l
```

List all current users (roles):

```
postgres=# \du
```

Create a new user (role) with a password:

```
CREATE ROLE databasename_user WITH LOGIN PASSWORD 'letmeintothisapp';
```

Create a new database and set the owner user(role):

``` bash
CREATE DATABASE databasename OWNER databasename_user;
```

Grant all privileges on the database to the database owner:

``` bash
GRANT ALL PRIVILEGES ON DATABASE databasename TO databasename_user;
```

Delete (drop) a database:

``` bash
postgres=# DROP DATABASE databasename;
```

Delete (drop) a user (role):

``` bash
postgres=# DROP ROLE databasename_user>;
```

Quit psql:

``` bash
postgres=# \q
```

Links:
* https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04



__Now Connect the postgres database__

By default the django project will use an sqlite database. Switch that out for the postgres database we created above in the project settings file by modifying the DATABASES section from

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

to

``` python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'skeletondb',
        'USER': 'skeletondb_user',
        'PASSWORD': 'letmeintothisapp',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

_Instead of putting the password directly into the file, it may be better to create a credentials.py file (in the top level folder) with db_password = 'mypassword', then import it at the top of settings.py and use it in the database section:_

``` python
import credentials as c
...
...
'PASSWORD': c.db_password,
```

Finally, run migrations to update the database

```
python manage.py makemigrations
python manage.py migrate
```

Again, you can check that things are going okay at this point by testing the development server runs the app okay (python manage.py runserver) - there now shouldn’t be complaints of unapplied migrations. 

__You can also delete db.sqlite3 at this point if it was created during initialisation.__