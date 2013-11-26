"""Factories for the ``test_app`` app."""
import factory

from django_libs.tests.factories import UserFactory

from .models import DummyModel, DummyProfileModel


class DummyModelFactory(factory.DjangoModelFactory):
    FACTORY_FOR = DummyModel

    name = factory.Sequence(lambda x: 'A name {0}'.format(x))


class DummyProfileModelFactory(factory.DjangoModelFactory):
    FACTORY_FOR = DummyProfileModel

    user = factory.SubFactory(UserFactory)
