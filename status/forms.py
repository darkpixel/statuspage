from django import forms
from django.forms import BaseFormSet
from django.forms.models import inlineformset_factory
from status.models import Incident, IncidentUpdate
from braces.forms import UserKwargModelFormMixin

import logging
logger = logging.getLogger(__name__)


IncidentFormset = inlineformset_factory(Incident, IncidentUpdate, min_num=1, validate_min=True, fields=('status', 'description'), can_delete=False, extra=0)


class IncidentCreateForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['name']

