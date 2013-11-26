"""Template tags of the ``privacy`` app."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library

from django_libs.loaders import load_member_from_setting

from ..models import PrivacyLevel, PrivacySetting

register = Library()


@register.inclusion_tag('privacy/partials/field.html')
def render_privacy_level_field(obj, field_name=None):
    kwargs = {
        'content_type': ContentType.objects.get_for_model(obj),
        'object_id': obj.pk,
    }
    if field_name:
        kwargs.update({'field_name': field_name})
    else:
        kwargs.update({'field_name': ''})
    privacy_levels = PrivacyLevel.objects.all()
    try:
        privacy_setting = PrivacySetting.objects.get(**kwargs)
    except PrivacySetting.DoesNotExist:
        kwargs.update({
            'level': privacy_levels.get(clearance_level=getattr(
                settings, 'PRIVACY_DEFAULT_CLEARANCE_LEVEL', 1)),
        })
        privacy_setting = PrivacySetting.objects.create(**kwargs)
    return {
        'field_name': field_name,
        'privacy_levels': privacy_levels,
        'privacy_setting': privacy_setting,
    }


def is_access_allowed(owner, requester, obj, field_name=None):
    get_clearance_level = load_member_from_setting(
        'PRIVACY_CLEARANCE_LEVEL_FUNCTION')
    clearance_level = get_clearance_level(owner, requester)
    kwargs = {
        'content_type': ContentType.objects.get_for_model(obj),
        'object_id': obj.pk,
    }
    if field_name:
        kwargs.update({'field_name': field_name})
    else:
        kwargs.update({'field_name': ''})
    try:
        privacy_setting = PrivacySetting.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return True  # No settings given? Allow for everyone
    if privacy_setting.level.clearance_level <= clearance_level:
        # Level has to be at least as high as the setting's label of the
        # object/field
        return True
    return False

register.assignment_tag(is_access_allowed)
