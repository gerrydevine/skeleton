from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()

TYPE_CHOICES = (
    ('THES', 'Thesis'),
    ('DATA', 'Dataset'),
    ('PUBL', 'Publication'),
    ('SOFT', 'Software'),
    ('NTRO', 'NTRO')
)

def validate_record_rating_1_10(value):
    ''' Validator function for Record Rating - Rating should be between 1 and 10 (if not None)'''
    if value is None:
        return value
    elif value > 0 and value <= 10:
        return value
    else:
        raise ValidationError("A rating should be between 1 and 10")
    

def validate_type(value):
    valid_types = [i[0] for i in TYPE_CHOICES]
    if value not in valid_types:
        raise ValidationError("Invalid Record Type")


class Record(models.Model):
    """Record Model"""

    # Fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, help_text='Enter Record Title', verbose_name='Record Title')
    description = models.TextField(help_text='Enter Record Description', verbose_name='Record Description')
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, help_text='Enter Record Type', verbose_name='Record Type', validators=[validate_type])
    rating = models.PositiveIntegerField(blank=True, null=True, default=None, help_text='Enter Rating (1-10)', validators =[validate_record_rating_1_10])
    version = models.FloatField(null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ['-updated']
        # permissions = (("can_bla_record", "Can bla record"),)

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of a Record."""
        return reverse('record-details', args=[str(self.id)])

    def __str__(self):
        return self.title


class RecordFile(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, help_text='Enter File Details', blank=True, null=True)
    description = models.TextField(help_text='Enter File Description', verbose_name='File Description')
    visible = models.BooleanField(default=True, help_text='Show this file on published record', verbose_name='File Visibility')
    uploaded = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.filename)

    class Meta:
        ordering = ["-updated"]
        verbose_name = "Record File"
        verbose_name_plural = "Record Files"
