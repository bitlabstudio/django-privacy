Django Privacy
==============

This is a generic app for assigning privacy related settings to whole objects
or to single fields.

If you add e.g. user profiles to your app, you might want to let the users
decide where and how to publish their content.
Some might want to hide everything from public, some might want to show private
updates to friends or colleagues only.

We define clearance levels to allow access or not. The lowest level is the
least secure. E.g.:

* Level 1: Everyone can see the content.
* Level 2: Only connected users can see the content.
* Level 3: Only the user herself can see the content.

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

PRIVACY_DEFAULT_CLEARANCE_LEVEL
+++++++++++++++++++++++++++++++

Default: 1

Default clearance level if a field has no privacy setting assigned.

Usage
-----

Template Tags
+++++++++++++

``is_access_allowed``

This assignment tag will check the relation of an object owner to the requester
and will return a ``True`` or ``False``. You can check the level for the whole
object or for a field of the object::

    {% load privacy_tags %}
    {% is_access_allowed object.user request.user object 'first_name' as access_allowed %}
    {% if access_allowed %}
        {{ object.first_name }}
    {% endif %}

--------------------------------------------------------------------------------

``render_privacy_level_field``

This inclusion tag will generate a privacy level next to your standard form
field::

    {% load privacy_tags %}
    {% render_privacy_level_field form.instance %}
    {% for field in form %}
        {{ field }} {% render_privacy_level_field form.instance field.field.name %}
    {% endfor %}

For carefree update forms use it with our ``PrivacyFormMixin`` (see below).


--------------------------------------------------------------------------------

``get_privacy_setting``

This assignment tag will return the current privacy setting::

    {% load privacy_tags %}
    {% get_privacy_setting form.instance 'name' as current_setting %}

The tag can be used with a field name or without to get the setting of the
whole object.


Form Mixin
++++++++++

``PrivacyFormMixin``

This form mixin handles privacy related form data (in case you use our
``render_privacy_level_field`` template tag). Just add the mixin class to your
form and privacy settings will be saved::

    from django import forms
    from privacy.forms import PrivacyFormMixin
    class MyModelForm(PrivacyFormMixin, forms.ModelForm):
        class Meta:
            model = MyModel
            fields = ('field1', 'field2')


Queryset helper
+++++++++++++++

If you want to filter querysets outside of templates (to keep pagination alive
or to use custom model managers), you can use the following helper:

``filter_privacy_level``

Just pass a ``queryset`` and a ``clearance_level``. You can also filter for
matching levels, just use ``exact``. An example::

    class MyListView(ListView):
        model = MyModel

        def get_queryset(self):
            qs = super(MyListView, self).get_queryset()
            clearance_level = get_clearance_level(self.owner, self.request.user)
            return filter_privacy_level(qs, clearance_level, self.request.GET.get('exact'))


Roadmap
-------

See the issue tracker for current and upcoming features.
