"""Factories for the ``test_app`` app."""
import factory

from .models import DummyModel


class DummyModelFactory(factory.DjangoModelFactory):
    FACTORY_FOR = DummyModel

    name = factory.Sequence(lambda x: 'A name {0}'.format(x))
