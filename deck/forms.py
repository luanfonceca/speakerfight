from django import forms

from .models import Event, Proposal


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ['event', 'author', 'rate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'inline-input'}),
        }