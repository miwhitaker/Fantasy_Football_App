from django import forms
from django.forms import HiddenInput

class DraftForm(forms.Form):
    player_id = forms.CharField(widget = HiddenInput(), label = '')
