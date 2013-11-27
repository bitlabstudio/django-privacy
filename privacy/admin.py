"""Admin for the ``privacy`` app."""
from django.contrib import admin

from hvad.admin import TranslatableAdmin

from .models import PrivacyLevel, PrivacySetting


admin.site.register(PrivacyLevel, TranslatableAdmin)
admin.site.register(PrivacySetting, admin.ModelAdmin)
