Django Privacy
==============

This is a generic app for assigning privacy related settings to whole objects
or to single fields.

If you add e.g. user profiles to your app, you might want to let the users
decide where and how to publish their content.
Some might want to hide everything from public, some might want to show private
updates to friends or colleagues only.

This app provides the backend for custom functions to (not) display content.

Prerequisites
-------------

You need at least the following packages in your virtualenv:

* Django >= 1.5
* django-hvad >= 0.3
* django-libs >= 1.27.1
* South


Installation
------------

To get the latest stable release from PyPi::

    $ pip install django-privacy

To get the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-privacy.git#egg=privacy

Add the app to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...
        'privacy',
    ]

Run the south migrations to create the app's database tables::

    $ ./manage.py migrate privacy

Settings
--------

PRIVACY_LEVEL_ORDERING
++++++++++++++++++++++

Default: ['clearance_level']

Ordering of the privacy levels. Use ``['-clearance_level']`` to reverse the
ordering or e.g. ``['name']`` to sort by level names.

PRIVACY_CLEARANCE_LEVEL_FUNCTION (mandatory)
++++++++++++++++++++++++++++++++++++++++++++

Default: None

Custom function to return a privacy level instance for the owner/requester
relation. E.g. ``'myproject.privacy_settings.get_clearance_level'``

You can find an example in the ``test_app`` of this repository.

Usage
-----

Template Tags
+++++++++++++

``is_access_allowed``

This assignment tag will check the relation of an object owner to the requester
and will return a ``True`` or ``False``. You can check the level for the whole
object or for a field of the object::

    {% is_access_allowed object.user request.user object 'first_name' as access_allowed %}
    {% if access_allowed %}
        {{ object.first_name }}
    {% endif %}

--------------------------------------------------------------------------------


Roadmap
-------

See the issue tracker for current and upcoming features.
