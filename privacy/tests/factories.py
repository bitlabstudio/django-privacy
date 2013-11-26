"""Factories for the ``privacy`` app."""
import factory

from django_libs.tests.factories import HvadFactoryMixin

from ..models import PrivacyLevel, PrivacySetting
from test_app.factories import DummyModelFactory


class PrivacyLevelFactory(HvadFactoryMixin, factory.DjangoModelFactory):
    FACTORY_FOR = PrivacyLevel

    language_code = 'en'
    name = factory.Sequence(lambda x: 'A name {0}'.format(x))
    clearance_level = factory.Sequence(lambda x: x)


class PrivacySettingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PrivacySetting

    level = factory.SubFactory(PrivacyLevelFactory)
    content_object = factory.SubFactory(DummyModelFactory)
