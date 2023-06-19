---
layout: default
title: Home
nav_order: 5
---

# Setting up a custom user

__Note - It is important to do this step before running the first migrate of the database as it can be difficult once the default user has already been set in place in the database__ 

We will override the default user model provided by Django (which requires a username) to only need an email as the required user field.

First thing we want to do is create a custom user that overrides the default django user. For the custom user, we will make it so that the email is the required field (and must be unique). Username will no longer be required.  

Start by creating a new 'app' for your custom user accounts

``` bash
$ python manage.py startapp users
```

Now create a new user model and manager that overrides the default abstract user model and user model manager

users/models.py:

``` python
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


    def __str__(self):
        return self.email

```

users/managers.py 

``` python
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """


    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
```

Now update the admin interface for the new user model. In users/admin.py, add the following:

``` python
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
```

Then add the new app to settings.py and update the AUTH_USER_MODEL setting to tell django to use this new custom user

``` python
INSTALLED_APPS = [
  ...
  'users',
]

AUTH_USER_MODEL = 'users.User'
```
 
Do a dry-run of the migration to check that the custom user model to be created looks correct:

``` bash
$ python manage.py makemigrations --dry-run --verbosity 3
```

Assuming things look good, go ahead with the migration (and create a superuser for the admin site):

``` bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

Now check out the admin site by logging in at .../admin (with the superuser account)
