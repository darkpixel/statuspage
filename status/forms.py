from django import forms
from status.models import Incident
from braces.forms import UserKwargModelFormMixin

import logging
logger = logging.getLogger(__name__)


class IncidentCreateForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['name', 'status', 'description']

    def save(self, force_insert=False, force_update=False, commit=True):
        logger.warn(self)
        logger.warn(dir(self))
        obj = super(IncidentCreateForm, self).save(commit=False)
        obj.user = self.user
        if commit:
            obj.save()
        return obj

