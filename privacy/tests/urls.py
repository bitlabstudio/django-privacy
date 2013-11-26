"""
This ``urls.py`` is only used when running the tests via ``runtests.py``.
As you know, every app must be hooked into yout main ``urls.py`` so that
you can actually reach the app's views (provided it has any views, of course).

"""
from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from django.views.generic import UpdateView

from test_app.forms import DummyProfileModelForm
from test_app.models import DummyProfileModel


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'(?P<pk>\d+)/',
        UpdateView.as_view(
            model=DummyProfileModel, form_class=DummyProfileModelForm),
        name='dummy_profile_update')
)
