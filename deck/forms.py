from django import forms
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from datetimewidget.widgets import DateTimeWidget

from .models import Event, Proposal, Activity


class CustomDateTimeWidget(DateTimeWidget):
    def format_output(self, *args, **kwargs):
        return super(CustomDateTimeWidget, self)\
            .format_output(*args, **kwargs).replace(
                '<i class="icon-th"></i>', '<i class="icon-th hide"></i>')


class CustomTimeInputWidget(forms.TimeInput):
    input_type = 'time'


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
    description = forms.CharField(required=True, widget=forms.Textarea())

    class Meta:
        model = Proposal
        exclude = [
            'event', 'author', 'track', 'rate',
            'is_approved', 'track_order',
            'activity_type', 'start_timetable', 'end_timetable',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
            'slides_url': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'jane_doe/talk',
                }),
        }


class ActivityForm(forms.ModelForm):
    # Removing the Proposal type from the available options
    activity_type = forms.ChoiceField(
        choices=[actitvity_type for actitvity_type in Activity.ACTIVITY_TYPES
                 if actitvity_type[0] != Activity.PROPOSAL])

    class Meta:
        model = Activity
        fields = [
            'title', 'description', 'activity_type',
            'start_timetable', 'end_timetable',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
            'start_timetable': CustomTimeInputWidget(format='%H:%M'),
            'end_timetable': CustomTimeInputWidget(format='%H:%M'),
        }


class ActivityTimetableForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'start_timetable', 'end_timetable',
        ]
        widgets = {
            'start_timetable': CustomTimeInputWidget(format='%H:%M'),
            'end_timetable': CustomTimeInputWidget(format='%H:%M'),
        }
