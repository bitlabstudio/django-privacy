"""Tests for the models of the ``privacy`` app."""
from django.test import TestCase

from .factories import (
    PrivacyLevelFactory,
    PrivacySettingFactory,
)
from ..models import filter_privacy_level
from test_app.factories import DummyModelFactory
from test_app.models import DummyModel


class PrivacyLevelTestCase(TestCase):
    """Tests for the ``PrivacyLevel`` model."""
    longMessage = True

    def setUp(self):
        self.privacy_level = PrivacyLevelFactory()

    def test_model(self):
        self.assertTrue(self.privacy_level.pk, msg=(
            'Should be able to instantiate and save the object.'))


class PrivacySettingTestCase(TestCase):
    """Tests for the ``PrivacySetting`` model."""
    longMessage = True

    def setUp(self):
        self.privacy_setting = PrivacySettingFactory()

    def test_model(self):
        self.assertTrue(self.privacy_setting.pk, msg=(
            'Should be able to instantiate and save the object.'))


class FilterPrivacyLevelTestCase(TestCase):
    """Tests for the ``filter_privacy_level`` helper function."""
    longMessage = True

    def setUp(self):
        self.dummy_1 = DummyModelFactory()
        self.dummy_2 = DummyModelFactory()
        self.dummy_3 = DummyModelFactory()

    def test_model(self):
        qs = []
        self.assertFalse(filter_privacy_level(qs, 4), msg=(
            'Should return the empty queryset, instead of raising an'
            ' exception, if queryset has no objects.'))
        qs = DummyModel.objects.all()
        self.assertEqual(filter_privacy_level(qs, 4).count(), 3, msg=(
            'Should return all objects, if they got no privacy settings.'))
        PrivacySettingFactory(content_object=self.dummy_1,
                              level__clearance_level=1)
        PrivacySettingFactory(content_object=self.dummy_2,
                              level__clearance_level=2)
        PrivacySettingFactory(content_object=self.dummy_3,
                              level__clearance_level=3)
        self.assertEqual(filter_privacy_level(qs, 1).count(), 1, msg=(
            'Should return only objects, which got level 1 or lower.'))
        self.assertEqual(filter_privacy_level(qs, 2).count(), 2, msg=(
            'Should return only objects, which got level 2 or lower.'))
        self.assertEqual(filter_privacy_level(qs, 3).count(), 3, msg=(
            'Should return only objects, which got level 3 or lower.'))
        self.assertEqual(filter_privacy_level(qs, 3, True).count(), 1, msg=(
            'Should return only objects, which got level 3 exactly.'))
