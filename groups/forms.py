from django import forms
from . import models


class GroupForm(forms.ModelForm):
    class Meta:
        fields = ("name", "description")
        model = models.Group

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs.update({'class':'form-control'})
