from django.apps import AppConfig
from django.conf import settings
from django.urls import path, include

from importlib import import_module


class DynamicFormBuilderConfig(AppConfig):
    name = 'dynamic_form_builder'

    def ready(self):
        patch_urls()


def patch_urls():
    """Sets automatically the url configuration for the project"""
    urlconf_module = import_module(settings.ROOT_URLCONF)
    urlconf_module.urlpatterns.append(path('dynamic_form_builder/', include('dynamic_form_builder.urls')))
