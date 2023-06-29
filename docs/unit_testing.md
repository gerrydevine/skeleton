---
layout: default
title: Unit testing
nav_order: 11
---

# Unit Testing

This section will show the basics of setting up and running unit tests on the newly created record model. Three tests are documented that cover:
- testing that a valid model gets successfully created
- testing that a invalid rating value gets properly rejected
- testing that an invalid type is rejected

Note that tests should only really be written for functionality developed in your code that is outside the default django.

In models/tests.py, add the below.

``` python
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Record
from users.models import User


class RecordModelTestcase(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(email="testuser1@gmail.com", password="abcd1234")


    def test_valid_record(self):
        """ Test that a record is created when provided valid data """

        user = User.objects.first()
        
        r = Record(owner = user, 
                    title = 'My new record', 
                    description = 'This is a description of this record', 
                    type='THES', 
                    rating=10, 
                    version=1.0)
        r.save()
        self.assertIsNotNone(r.id)


    def test_invalid_rating(self):
        """ Test that a validation error occurs when rating is not between 1 and 10 """

        user = User.objects.first()
        
        r = Record(
            owner = user, 
            title = 'My new record', 
            description = 'This is a description of this record', 
            type='THES', 
            rating=15, 
            version=1.0
        )

        with self.assertRaises(ValidationError):
            r.save()


    def test_invalid_type(self):
        """ Test that a validation error occurs when rating is not between 1 and 10 """

        user = User.objects.first()
        
        r = Record(
            owner = user, 
            title = 'My new record', 
            description = 'This is a description of this record', 
            type='THESIS', 
            rating=10, 
            version=1.0
        )

        with self.assertRaises(ValidationError):
            r.save()
```

Run the test:

```bash
$ python manage.py test
```

You should hopefully get three passing tests:

```bash
Found 3 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran 3 tests in 0.038s

OK
Destroying test database for alias 'default'...
```
