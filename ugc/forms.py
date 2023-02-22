from django import forms
from django.forms import CharField
from .models import Profile, validate_hash, Message


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('external_id', 'name')
        widgets = {"name": forms.TextInput, }


class MessageForm(CharField):
    default_validators = [validate_hash]

    class Meta:
        model = Message
        fields = "__all__"
