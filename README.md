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


# Usage

- In your `models.py`:

```python
from dynamic_form_builder.models import FormBuilderField

class MyModel(models.Model):
    # foreign key to the template to select
    template = FormBuilderField(limit_to_model='mymodel',
                                null=True, blank=True)
    # the field to store the filled form
    my_dyn_field = models.CharField(max_length=2000, null=True, blank=True)
```

- In your `views.py`, you will have to use `DynamicFormBuilderViewMixin`:

```python
from dynamic_form_builder.views import DynamicFormBuilderViewMixin


class MyModelCreate(DynamicFormBuilderViewMixin, CreateView):
    model = models.MyModel
    form_class = forms.MyModelForm
    dynamic_field = 'my_dyn_field'


class MyModelUpdate(DynamicFormBuilderViewMixin, UpdateView):
    model = models.MyModel
    form_class = forms.MyModelForm
    dynamic_field = 'my_dyn_field'


class MyModelDetail(DynamicFormBuilderViewMixin, DetailView):
    model = models.MyModel
    dynamic_field = 'my_dyn_field'

```

- In your form template, you will have to add a new tag:
`overridable_table_form json`:

```
{% extends "common.html" %}
{% load overridable_form %}

{% block title %} Post Project {% endblock %}

{% block body %}

    <form action="" method="post" enctype="multipart/form-data" id="postform">
        <table>
            {% csrf_token %}
            {{ form.as_table }}
        </table>
        {% overridable_table_form json_form %}
        <input type="submit" value="Submit" />
    </form>

{% endblock %}
```

- For your detail template, acces the dynamic form data trough
the tag `dyn_form_data`:

```
{% for field, value in dyn_form_data.items %}
        <tr>
            <th>{{ field }} </th> <td>{{ value }}</td>
        </tr>
{% endfor %}
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
