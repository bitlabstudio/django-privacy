"""Admin for the ``test_app`` app."""
from django.contrib import admin

from .models import DummyProfileModel


admin.site.register(DummyProfileModel)
