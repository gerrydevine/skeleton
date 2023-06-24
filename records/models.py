from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

# validator function for Record - rating should be between 1 and 10
def validate_record_rating_1_10(value):
    if value > 0 and value <= 10:
        return value
    else:
        raise ValidationError("A rating should be between 1 and 10")


class Record(models.Model):
    """Record Model"""

    TYPE_CHOICES = (
        ('THES', 'THESIS'),
        ('DATA', 'DATASET'),
        ('PUBL', 'PUBLICATION'),
        ('NTRO', 'NON-TRADITIONAL RESEARCH OUTPUT')
    )

    # Fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, help_text='Enter Record Title', verbose_name='Record Title')
    description = models.TextField(help_text='Enter Record Description', verbose_name='Record Description')
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, help_text='Enter Record Type', verbose_name='Record Type')
    rating = models.IntegerField(blank=True, null=True, default=None, help_text='Enter Rating (1-10)', validators =[validate_record_rating_1_10])
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

        