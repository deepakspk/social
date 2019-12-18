from .models import Msg, Member
from django.forms import ModelForm
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

    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         for field in self.fields:
             self.fields[field].widget.attrs.update({'class':'form-control'})
