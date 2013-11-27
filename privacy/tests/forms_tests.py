"""Tests for the forms of the ``privacy`` app."""
from django.test import TestCase

from .factories import PrivacyLevelFactory, PrivacySettingFactory
from ..models import PrivacySetting
from test_app.factories import DummyProfileModelFactory
from test_app.forms import DummyProfileModelForm


class DummyProfileModelFormTestCase(TestCase):
    """Tests for the ``DummyProfileModelForm`` form."""
    longMessage = True

    def setUp(self):
        self.obj = DummyProfileModelFactory()
        self.level_1 = PrivacyLevelFactory(clearance_level=1)
        self.level_2 = PrivacyLevelFactory(clearance_level=2)
        self.level_3 = PrivacyLevelFactory(clearance_level=3)
        self.level_4 = PrivacyLevelFactory(clearance_level=4)
        self.field_setting = PrivacySettingFactory(
            content_object=self.obj, level=self.level_1, field_name='name')

    def test_tag(self):
        data = {
            'user': self.obj.user.pk,
            'privacy_for_instance': 3,
        }
        form = DummyProfileModelForm(instance=self.obj, data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))
        form.save()
        self.setting = PrivacySetting.objects.get(
            object_id=self.obj.pk, field_name='')
        self.assertEqual(self.setting.level, self.level_3, msg=(
            'The form instance\'s privacy setting should be set to 3.'))
        data.update({'privacy_name': 4})
        form = DummyProfileModelForm(instance=self.obj, data=data)
        self.assertTrue(form.is_valid(), msg=('Form should be valid.'))
        form.save()
        self.assertEqual(
            PrivacySetting.objects.get(pk=self.field_setting.pk).level,
            self.level_4,
            msg=('The name field\'s privacy setting should be set to 3.'))
