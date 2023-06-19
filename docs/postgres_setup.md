---
layout: default
title: Postgres Setup
nav_order: 6
---

# Postgres Setup

Let’s get our database set up. We will use postgres as the underlying database during development (as opposed to sqlite3).

Make sure postgres/psql is installed (and optionally include a GUI like pgadmin) 

Enter psql mode (and by default connecting to the postgres database with the postgres user ):

``` bash
$ psql -d postgres -U gerrydevine
```

(you can force user and/or database to connect to using -U and -d)

Use \du and \l to list current postgres users/roles and current databases respectively:

``` bash
postgres=# \du
postgres=# \l
```


Add a new postgres user/role to manage our new database (I like to have a seperate user/role for each app/database):

``` bash
postgres=# CREATE ROLE myapp_dbadmin WITH LOGIN PASSWORD 'my_password';
```

(Note: You should have your default postgres and normal user postgres accounts locked down with a password - they are superusers by default)

Allow this new user to have ‘CreateDB’ ability:

```
postgres=# ALTER ROLE myapp_dbadmin CREATEDB;
```

To create a new (dedicated) database for our app, log out of psql (\q) and back in again (as the new user)

``` bash
postgres=# \q
$ psql postgres -U myapp_dbadmin
```

Now create the database, and assign the app user/role superuser privileges on the new database:

``` bash
postgres=> CREATE DATABASE myapp_devdb;
postgres=> GRANT ALL PRIVILEGES ON DATABASE myapp_devdb TO myapp_dbadmin;
```

Now check that the setup is correct by listing the databases (\l) and checking that the right database is in place with the right user who has the right privileges:

``` bash
postgres=> \l
myapp_devdb             | myapp_dbadmin | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/myapp_dbadmin                +
                        |               |          |             |             | myapp_dbadmin=CTc/myapp_dbadmin
```

Assuming everything is good, exit psql:

``` bash
postgres=> \q
```

You can delete databases and users(roles), assuming the current psql user has the rights to, using:

``` bash
postgres=> DROP DATABASE database_name;
postgres=> DROP ROLE user_name;
```

Now Connect the postgres database. By default the django project will use an sqlite database. Switch that out for the postgres database we created above in the project settings_dev.py file by modifying the DATABASES section from

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
        'NAME': 'myapp_devdb',
        'USER': 'myapp_dbadmin',
        'PASSWORD': 'myapp_dbpw',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

** Instead of putting the password directly into the file, it may be better to create a credentials.py file (in the top level folder) with db_password = 'mypassword', then import it at the top of settings.py and use it in the database section:

``` python
import credentials as c
...
...
'PASSWORD': c.db_password,
```

Finally, run migrations to update the database

``` bash
python manage.py migrate
```

Again, you can check that things are going okay at this point by testing the development server runs the app okay (python manage.py runserver) - there now shouldn’t be complaints of unapplied migrations. 

You can also delete db.sqlite3 at this point if it was created during initialisation.
