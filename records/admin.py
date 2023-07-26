from django.contrib import admin
from .models import Record
from django.core.exceptions import ValidationError
from django.forms import ModelForm

 
class RecordForm(ModelForm):
       
   def clean(self):       
      errors={}
      if 'private' in self.cleaned_data['title'].lower():
         errors['title']= ('Sensitive Titles are not allowed')
      if Record.objects.filter(owner=self.cleaned_data['owner'], title=self.cleaned_data['title']).exists():
         errors['title'] = ('A matching title already exists for that user.')
      if errors:
         raise ValidationError(errors)
 
 
class RecordAdmin(admin.ModelAdmin):
   form = RecordForm
   fields = ('owner', 'title', 'description', 'type', 'rating', 'version')
 
 
admin.site.register(Record, RecordAdmin)