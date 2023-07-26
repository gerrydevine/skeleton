from django import forms
from django.forms import Form, ModelForm
from django.core.exceptions import ValidationError
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
        if Record.objects.filter(owner=self.request.user, title=title).exists():
            self.add_error('title', 'You have used this title already!')
        
        return cleaned_data


# class RecordForm(forms.Form):
#     title = forms.CharField()
#     description = forms.CharField()
#     type = forms.CharField()    

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super(RecordForm, self).__init__(*args, **kwargs)

#     def clean(self):
#         cleaned_data = self.cleaned_data

#         title = cleaned_data.get('title')

#         if Record.objects.filter(owner=self.user, title=title).exists():
#             self.add_error('title', 'You have used this title already!')
        
#         return cleaned_data
    

class RecordCreateForm(ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'description', 'type', 'rating', 'version']
    
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')

        super(RecordCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RecordCreateForm, self).clean()

        title = cleaned_data.get('title')

        if Record.objects.filter(owner=self.owner, title=title).exists():
            self.add_error(None, ValidationError('You have used this title already!'))


class RecordUpdateForm(ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'description', 'type', 'rating', 'version']
    
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')

        super(RecordUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RecordUpdateForm, self).clean()

        title = cleaned_data.get('title')

        other_records = Record.objects.filter(owner=self.owner).exclude(pk=self.instance.pk)

        if other_records.filter(title=title).exists():
            self.add_error(None, ValidationError('You have used this title already!'))
