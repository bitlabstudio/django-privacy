"""Forms for the ``privacy`` app."""
from django.contrib.contenttypes.models import ContentType

from .models import PrivacyLevel, PrivacySetting


class PrivacyFormMixin(object):
    """Form mixin for forms with privacy level fields."""
    def save(self, *args, **kwargs):
        instance = super(PrivacyFormMixin, self).save(*args, **kwargs)
        for key in self.data.keys():
            if not key.startswith('privacy_'):
                continue
            field_name = key.replace('privacy_', '')
            if field_name == 'for_instance':
                field_name = ''
            ctype = ContentType.objects.get_for_model(self.instance)
            privacy_setting = PrivacySetting.objects.get(
                content_type=ctype, object_id=self.instance.pk,
                field_name=field_name)
            privacy_setting.level = PrivacyLevel.objects.get(
                clearance_level=self.data[key])
            privacy_setting.save()
        return instance
