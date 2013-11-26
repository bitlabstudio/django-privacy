"""Forms for the ``test_app`` app."""
from django import forms

from .models import DummyProfileModel
from privacy.forms import PrivacyFormMixin


class DummyProfileModelForm(PrivacyFormMixin, forms.ModelForm):
    class Meta:
        model = DummyProfileModel
        fields = ('user', )
