from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from deck.models import Event


class InviteForm(forms.ModelForm):
    email = forms.EmailField(label=_('User email'))

    class Meta:
        model = Event
        fields = []

    def add_to_jury(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                _(u'The "%s" are not a Speakerfight user. '
                  u'For now, we just allow already joined users.') % email)
        if self.instance.jury.users.filter(pk=user.pk).exists():
            raise ValidationError(
                _(u'The "@%s" already is being part of this jury.') % user)
        self.instance.jury.users.add(user)
