from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from datetimewidget.widgets import DateTimeWidget

from .models import Event, Proposal


class CustomDateTimeWidget(DateTimeWidget):
    def format_output(self, *args, **kwargs):
        return super(CustomDateTimeWidget, self)\
            .format_output(*args, **kwargs).replace(
                '<i class="icon-th"></i>', '<i class="icon-th hide"></i>')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['author', 'jury']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
            'due_date': CustomDateTimeWidget(attrs={
                'id': 'id_due_date',
                'class': 'inline-input',
                'placeholder': 'Due Date'
            }),
        }


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


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ['event', 'author', 'rate', 'is_approved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
        }
