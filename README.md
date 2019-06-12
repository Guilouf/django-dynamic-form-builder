# django-dynamic-form-builder
Django reusable app to create dynamic forms from the admin interface
and save them into a specific model field

# Installation
`pip install .` from the root folder

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
