---
layout: default
title: Initial Django Setup
parent: Setup
nav_order: 1
---

# Initial Django Setup

Create and navigate to the outer development directory, e.g. dev/django/ (or wherever you want to store the Django project):

``` bash
$ cd dev/django/
```

Create a new Project folder (here called skeleton) and cd into it:

``` bash
$ mkdir skeleton
$ cd skeleton
```

Set up a python 3 venv environment for this project (called env) and activate it:

``` bash
$ python3 -m venv .venv
$ . .venv/bin/activate
```

Use pip to install the initial required python packages into this active pipenv environment (the main django library, postgres library, and some linting libraries)

``` bash
$ pip install wheel django djangorestframework psycopg2 pylint pep8 autopep8
```

Now lock the packages into a 'requirements.txt' file 

``` bash
$ pip freeze > requirements.txt
```

Now turn the current folder into a Django project using the django-admin.py tool

``` bash
$ django-admin startproject main .
```

This creates a default 'app' called main and the . turns the current folder into the Django project.

You can check that your basic Django app is up and running at this point by running:

``` bash
$ python manage.py runserver
```

and then visiting http://127.0.0.1:8000 in your browser. Don’t worry about the terminal complaining of unapplied migrations at this point - we will fix that in later steps.

At this point you can move to working inside Visual Code Studio: (see next section)

``` bash
$ code .
```

Now add psycopg2 to INSTALLED_APPS in the project settings file, which is the 'main' app folder inside your backend folder (backend/main/settings.py):

``` python
INSTALLED_APPS = [
    ...,
    psycopg2 
]
```
