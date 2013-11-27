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
            kwargs = {
                'content_type': ctype,
                'object_id': self.instance.pk,
                'field_name': field_name,
            }
            level = PrivacyLevel.objects.get(clearance_level=self.data[key])
            try:
                privacy_setting = PrivacySetting.objects.get(**kwargs)
            except PrivacySetting.DoesNotExist:
                kwargs.update({'level': level})
                privacy_setting = PrivacySetting.objects.create(**kwargs)
            else:
                privacy_setting.level = level
                privacy_setting.save()
        return instance
