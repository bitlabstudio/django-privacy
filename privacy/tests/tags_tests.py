"""Tests for the template tags of the ``privacy`` app."""
from django.template import Context, Template
from django.test import TestCase

from ..templatetags.privacy_tags import is_access_allowed, get_privacy_setting
from .factories import PrivacyLevelFactory, PrivacySettingFactory
from test_app.factories import DummyProfileModelFactory, DummyModelFactory


class GetPrivacySettingTestCase(TestCase):
    """Tests for the ``get_privacy_setting`` filter tag."""
    longMessage = True

    def setUp(self):
        self.obj = DummyModelFactory()
        self.level_1 = PrivacyLevelFactory(clearance_level=1)
        self.level_2 = PrivacyLevelFactory(clearance_level=2)

    def test_tag(self):
        self.assertIsNone(get_privacy_setting(self.obj), msg=(
            'Should return None, if there\'s no setting set.'))
        PrivacySettingFactory(level=self.level_1, content_object=self.obj)
        self.assertEqual(
            get_privacy_setting(self.obj).level.clearance_level, 1, msg=(
                'Should return the privacy setting.'))


class RenderPrivacyLevelFieldTestCase(TestCase):
    """Tests for the ``render_privacy_level_field`` inclusion tag."""
    longMessage = True

    def setUp(self):
        self.obj = DummyModelFactory()
        self.level_1 = PrivacyLevelFactory(clearance_level=1)
        self.level_2 = PrivacyLevelFactory(clearance_level=2)

    def test_tag(self):
        t = Template(
            '{% load privacy_tags %}{% render_privacy_level_field obj %}')
        c = Context({'obj': self.obj})
        self.assertIn('name="privacy_for_instance"', t.render(c))
        t = Template('{% load privacy_tags %}{% render_privacy_level_field obj'
                     ' "name" %}')
        self.assertIn('name="privacy_name"', t.render(c))


class IsAccessAllowedTestCase(TestCase):
    """Tests for the ``is_access_allowed`` assignment tag."""
    longMessage = True

    def setUp(self):
        self.level_1 = PrivacyLevelFactory(clearance_level=1)
        self.level_2 = PrivacyLevelFactory(clearance_level=2)
        self.level_3 = PrivacyLevelFactory(clearance_level=3)
        self.level_4 = PrivacyLevelFactory(clearance_level=4)
        self.owner = DummyProfileModelFactory()
        self.requester = DummyProfileModelFactory()
        self.obj = DummyModelFactory()

    def test_tag(self):
        # No level
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should be allowed, if it\'s an object without privacy'
                 ' setting.'))

        # Level 1
        setting = PrivacySettingFactory(
            level=self.level_1, content_object=self.obj)
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should be allowed, if it\'s a public object.'))

        # Level 2
        setting.level = self.level_2
        setting.save()
        self.assertFalse(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should not be allowed, if the requester is not at'
                 ' least a friend of a friend.'))
        friend = DummyProfileModelFactory()
        self.owner.friends.add(friend.user)
        self.requester.friends.add(friend.user)
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should be allowed, if the requester is at least a'
                 ' friend of a friend.'))

        # Level 3
        setting.level = self.level_3
        setting.save()
        self.assertFalse(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should not be allowed, if the requester is not at'
                 ' least a friend.'))
        self.owner.friends.add(self.requester.user)
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should be allowed, if the requester is at least a'
                 ' friend.'))

        # Level 4
        setting.level = self.level_4
        setting.save()
        self.assertFalse(
            is_access_allowed(self.owner, self.requester, self.obj),
            msg=('Access should only be allowed, if the requester is also the'
                 ' owner.'))
        self.assertTrue(
            is_access_allowed(self.owner, self.owner, self.obj),
            msg=('Access should only be allowed, if the requester is also the'
                 ' owner.'))

    def test_tag_with_field_name(self):
        # No level
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj, 'name'),
            msg=('Access should be allowed, if it\'s an object without privacy'
                 ' setting.'))

        # Level 1
        setting = PrivacySettingFactory(
            level=self.level_1, content_object=self.obj, field_name='name')
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj, 'name'),
            msg=('Access should be allowed, if it\'s a public object.'))

        # Level 2
        setting.level = self.level_2
        setting.save()
        self.assertFalse(
            is_access_allowed(self.owner, self.requester, self.obj, 'name'),
            msg=('Access should not be allowed, if the requester is not at'
                 ' least a friend of a friend.'))
        friend = DummyProfileModelFactory()
        self.owner.friends.add(friend.user)
        self.requester.friends.add(friend.user)
        self.assertTrue(
            is_access_allowed(self.owner, self.requester, self.obj, 'name'),
            msg=('Access should be allowed, if the requester is at least a'
                 ' friend of a friend.'))
