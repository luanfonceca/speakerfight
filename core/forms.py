# from django.contrib.auth.models import User

from django import forms

from core.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
