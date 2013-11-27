"""Models for the ``privacy`` app."""
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields


def filter_privacy_level(qs, clearance_level, exact=False):
    """
    Function to exclude objects from a queryset, which got a higher clearance
    level than the wanted maximum clearance level.

    :qs: Django queryset.
    :clearance_level: Minimum clearance level.
    :exact: Boolean to check for the exact clearance level.

    """
    if not qs:
        return qs
    c_type = ContentType.objects.get_for_model(qs.model)
    kwargs = {
        'content_type': c_type,
        'object_id__in': qs.values_list('pk'),
        'level__clearance_level{}'.format(
            '' if exact else '__gt'): clearance_level,
    }
    private_objects = PrivacySetting.objects.filter(**kwargs).values_list(
        'object_id')
    if exact:
        return qs.filter(pk__in=private_objects)
    return qs.exclude(pk__in=private_objects)


class PrivacyLevel(TranslatableModel):
    """
    Privacy level, which defines the assessment factor.

    :name: Translatable name of the privacy level.
    :clearance_level: Privacy level (the higher the more secure).

    """
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
    )

    clearance_level = models.IntegerField(
        unique=True,
        verbose_name=_('Clearance level'),
    )

    class Meta:
        ordering = getattr(
            settings, 'PRIVACY_LEVEL_ORDERING', ['clearance_level'])

    def __unicode__(self):
        return self.safe_translation_getter(
            'name', self.translations.all()[0].name)


class PrivacySetting(models.Model):
    """
    Privacy setting, which defines one custom setting for one object.

    :content_object: Related secured object.
    :level: Connection to the PrivacyLevel model.
    :field_name: Optional field_name to limit the setting to a single field.

    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    level = models.ForeignKey(
        PrivacyLevel,
        verbose_name=_('Privacy level'),
    )

    field_name = models.CharField(
        max_length=50,
        verbose_name=_('Field name'),
        blank=True,
    )

    def __unicode__(self):
        return '{} - {}'.format(self.content_object, self.level)
