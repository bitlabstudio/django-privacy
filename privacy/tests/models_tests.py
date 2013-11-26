"""Tests for the models of the ``privacy`` app."""
from django.test import TestCase

from .factories import (
    PrivacyLevelFactory,
    PrivacySettingFactory,
)


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
