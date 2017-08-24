# from django.contrib.auth.models import User

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from core.models import Profile


class ProfileForm(forms.ModelForm):
    username = forms.CharField(
        label=_('Username'), max_length=200, required=True)
    name = forms.CharField(label=_('Name'), max_length=200, required=True)
    email = forms.EmailField(label=_('Email'), max_length=200, required=True)

    class Meta:
        model = Profile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        full_name = self.instance.user.get_full_name()
        email = self.instance.user.email
        username = self.instance.user.username

        self.fields['name'].initial = full_name
        self.fields['email'].initial = email
        self.fields['username'].initial = username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username == self.instance.user.username:
            return username

        if User.objects.filter(username=username).exists():
            message = _(
                u'The "%s" username are already being used by someone.'
            ) % username
            raise ValidationError(message)

        return username

    def save(self, *args, **kwargs):
        self.save_user_data()
        return super(ProfileForm, self).save(*args, **kwargs)

    def save_user_data(self):
        data = self.cleaned_data

        if data.get('name') != self.instance.user.get_full_name():
            first_name = data.get('name').split()[0]
            last_name = ' '.join(data.get('name').split()[1:])
            self.instance.user.first_name = first_name
            self.instance.user.last_name = last_name

        if data.get('email') != self.instance.user.email:
            self.instance.user.email = data.get('email')

        if data.get('username') != self.instance.user.username:
            self.instance.user.username = data.get('username')

        self.instance.user.save()


class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image',)
