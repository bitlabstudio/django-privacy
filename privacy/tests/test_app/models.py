"""Dummy models to be used in test cases of the ``privacy`` app."""
from django.core.urlresolvers import reverse
from django.db import models


class DummyModel(models.Model):
    """Dummy to be used in test cases of the ``privacy`` app."""
    name = models.CharField(max_length=256, blank=True)
    privacy = models.ForeignKey(
        'privacy.PrivacySetting', blank=True, null=True)

    def __unicode__(self):
        return self.name


class DummyProfileModel(models.Model):
    """Dummy profile to be used in test cases of the ``privacy`` app."""
    user = models.ForeignKey('auth.User', related_name='dummy_profiles')
    friends = models.ManyToManyField('auth.User', blank=True, null=True,
                                     related_name='friended_dummy_profiles')

    def get_absolute_url(self):
        return reverse('dummy_profile_update', kwargs={'pk': self.pk})
