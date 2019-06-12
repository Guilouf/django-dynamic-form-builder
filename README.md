# django-dynamic-form-builder
Django reusable app to create dynamic forms from the admin interface
and save them into a specific model field

# Installation
From the root folder:

```
pip install .
```

You have to do a bit of configuration from the host project:
- In your `settings.py`:

```python
INSTALLED_APPS = (
    # other apps
    'dynamic_form_builder',
)


# Your app that you want to use dynamic-form-builder with
DYNAMIC_FORM_BUILDER_TARGET = 'your_app'
```


urlpatterns = [
    # other urls patterns
    path('some_string/', include('dynamic_form_builder.urls')),
]
```



# Developement
Be sure to push migrations after any change into the models, for
standalone apps like this project you can use this script:

```python
import django
from django.conf import settings
from django.core.management import call_command

settings.configure(DEBUG=True,
                   INSTALLED_APPS=(
                       'django.contrib.contenttypes',
                       'dynamic_form_builder',
                   ),
                   )

django.setup()
call_command('makemigrations', 'dynamic_form_builder')

```
