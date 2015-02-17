from django import forms
from status.models import Incident, IncidentUpdate
from braces.forms import UserKwargModelFormMixin

import logging
logger = logging.getLogger(__name__)


class IncidentUpdateCreateForm(forms.ModelForm):
    class Meta:
        model = IncidentUpdate
        fields = ['status', 'description']


class IncidentCreateForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['name']
