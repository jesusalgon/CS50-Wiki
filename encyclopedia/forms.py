from django import forms
from django.core.exceptions import ValidationError
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':  'mb-3'}), label="New Entry Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in util.list_entries():
            raise ValidationError('An entry with this title already exists. Please, provide a new title.')

        return title


class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")
