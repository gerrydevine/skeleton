---
layout: default
title: Model Setup
nav_order: 8
---

# Model Setup

For the remainder of this tutorial we will use the idea of a record system. A user can create, view, edit and delete a record. They will also be able to publish the record when ready, thus making it visible by all (inc non-logged in users). In addition, the user can nominate other users to be able to collaborate on the record. A reviewer role will review the published record before it is made public.  


## New Model

The structure of a new model will typically take the following form: 

```python
from django.db import models
from django.urls import reverse

class MyModelName(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    # …

    # Metadata
    class Meta:
        ordering = ['-my_field_name']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.my_field_name
```

### COMMON FIELD ARGUMENTS

(From developer.mozilla)

The following common arguments can be used when declaring many/most of the different field types:

- __help_text__: Provides a text label for HTML forms (e.g. in the admin site), as described above.
verbose_name: A human-readable name for the field used in field labels. If not specified, Django will infer the default verbose name from the field name.
- __default__: The default value for the field. This can be a value or a callable object, in which case the object will be called every time a new record is created.
- __null__: If True, Django will store blank values as NULL in the database for fields where this is appropriate (a CharField will instead store an empty string). The default is False.
- __blank__: If True, the field is allowed to be blank in your forms. The default is False, which means that Django's form validation will force you to enter a value. This is often used with null=True, because if you're going to allow blank values, you also want the database to be able to represent them appropriately.
- __choices__: A group of choices for this field. If this is provided, the default corresponding form widget will be a select box with these choices instead of the standard text field.
- __primary_key__: If True, sets the current field as the primary key for the model (A primary key is a special database column designated to uniquely identify all the different table records). If no field is specified as the primary key, Django will automatically add a field for this purpose. The type of auto-created primary key fields can be specified for each app in AppConfig.default_auto_field or globally in the DEFAULT_AUTO_FIELD setting.

## Record App

We first need to create our _Record_ App:

```bash
$ python manage.py startapp records
```

Now register it in INSTALLED_APPS in settings.py

### Record Model

Create a new Record Model. Note that we are importing the User model here so that we can associate the Record with an Owner User.

```python
class Record(models.Model):
    """Record Model"""

    TYPE_CHOICES = [
        'THES', 'THESIS',
        'DATA', 'DATASET',
        'PUBL', 'PUBLICATION',
        'NTRO', 'NON-TRADITIONAL RESEARCH OUTPUT'
    ]

    # Fields
    owner = models.ForeignKey(User, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, help_text='Enter Record Title', verbose_name='Record Title')
    description = models.TextField(help_text='Enter Record Description', verbose_name='Record Description')
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, help_text='Enter Record Type', verbose_name='Record Type')
    rating = models.IntegerField(blank=True, null=True, default=None)
    version = models.FloatField(null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        ordering = ['-updated']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of a Record."""
        return reverse('record-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the Record object (in Admin site etc.)."""
        return self.title
```