"""Dummy models to be used in test cases of the ``privacy`` app."""
from django.db import models


class DummyModel(models.Model):
    """Dummy to be used in test cases of the ``privacy`` app."""
    name = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.name
