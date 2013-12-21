"""Template tags of the ``privacy`` app."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library

from django_libs.loaders import load_member_from_setting

from ..models import PrivacyLevel, PrivacySetting

register = Library()


def get_privacy_dict(obj, field_name):
    """
    Function, which returns a dictionary of relevant data of a privacy level
    (field).

    """
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
        selected_setting = PrivacySetting.objects.get(**kwargs)
        selected_level = selected_setting.level.clearance_level
    except PrivacySetting.DoesNotExist:
        selected_setting = None
        selected_level = getattr(
            settings, 'PRIVACY_DEFAULT_CLEARANCE_LEVEL', 1)
    return {
        'field_name': field_name,
        'privacy_levels': privacy_levels,
        'selected_level': selected_level,
        'selected_setting': selected_setting,
    }


@register.assignment_tag
def get_privacy_setting(obj, field_name=None):
    privacy_dict = get_privacy_dict(obj, field_name)
    return privacy_dict['selected_setting']


@register.inclusion_tag('privacy/partials/field.html')
def render_privacy_level_field(obj, field_name=None):
    return get_privacy_dict(obj, field_name)


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
