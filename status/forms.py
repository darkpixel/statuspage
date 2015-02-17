from django import forms
from django.forms import BaseFormSet
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from status.models import Incident, IncidentUpdate
from braces.forms import UserKwargModelFormMixin

import logging
logger = logging.getLogger(__name__)


class IncidentFormsetBase(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(IncidentFormsetBase, self).__init__(*args, **kwargs)
        self.fields['user'].initial = self.user

    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            self.forms.append(self._construct_form(i, user=self.user))


IncidentFormset = inlineformset_factory(Incident, IncidentUpdate, formset=IncidentFormsetBase, min_num=1, validate_min=True, fields=('status', 'description'), can_delete=False, extra=0)


class IncidentCreateForm(UserKwargModelFormMixin, forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['name']

