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
postgres=# DROP DATABASE databasename_user>;
```

Quit psql:

``` bash
postgres=# \q
```

Links:
* https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04