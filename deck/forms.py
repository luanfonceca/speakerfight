from django import forms

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
        exclude = ['author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
            'due_date': CustomDateTimeWidget(attrs={'id': 'id_due_date'})
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ['event', 'author', 'rate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
        }
