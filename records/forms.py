from django import forms
# from django.forms import Form, ModelForm
# from django.core.exceptions import ValidationError
from records.models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'description', 'type', 'rating', 'version']
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RecordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        # Clean title
        title = cleaned_data.get('title')

        if self.instance.pk:
            records = Record.objects.filter(owner=self.request.user, title=title).exclude(pk=self.instance.pk)
            if records.exists():
                self.add_error('title', 'You have used this title already!')
        else:
            records = Record.objects.filter(owner=self.request.user, title=title)
            if records.exists():
                self.add_error('title', 'You have used this title already!')
        
        return cleaned_data


# class RecordUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Record
#         fields = ['title', 'description', 'type', 'rating', 'version']
    
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request")
#         super(RecordUpdateForm, self).__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = self.cleaned_data

#         # Clean title
#         title = cleaned_data.get('title')

#         other_records = Record.objects.filter(owner=self.request.user).exclude(pk=self.instance.pk)
#         if other_records.filter(title=title).exists():
#             self.add_error('title', 'You have used this title already!')
        
#         return cleaned_data
