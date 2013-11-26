"""Tests for the template tags of the ``privacy`` app."""
from django.test import TestCase

from ..templatetags.privacy_tags import is_access_allowed
from .factories import PrivacyLevelFactory, PrivacySettingFactory
from test_app.factories import DummyProfileModelFactory, DummyModelFactory


class IsAccessAllowedTestCase(TestCase):
    """Tests for the ``is_access_allowed`` filter."""
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
