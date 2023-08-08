from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Record
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
