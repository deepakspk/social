from .models import Msg, Member
from django.forms import ModelForm, Form
from django import forms


class MsgForm(ModelForm):
    class Meta:
        model= Msg
        fields = '__all__'

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs.update({'class':'form-control'})


class MemberForm(ModelForm):
    class Meta:
        model= Member
        fields = '__all__'
        widgets = {
            'joined_on':forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs.update({'class':'form-control'})

class contact_form(forms.Form):
    contact_name = forms.CharField(label='Contact Name', max_length=255)
    contact_email = forms.CharField(label='Contact Email',max_length=255)
    contact_message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
