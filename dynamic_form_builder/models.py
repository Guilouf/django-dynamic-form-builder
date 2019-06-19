from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings

import yaml
from dynamic_form_builder.forms import FormBuilderFormField


def choice_limit():
    """Get the 'DYNAMIC_FORM_BUILDER_TARGETS' constant from the settings file to display
    models from the targeted app"""
    return {'app_label': getattr(settings, 'DYNAMIC_FORM_BUILDER_TARGET', None)}


class FormBuilderField(models.ForeignKey):

    def __init__(self, **kwargs):
        """Sets default field's related model and deletion method"""
        kwargs.setdefault('to', 'dynamic_form_builder.DescriptorTemplate')
        kwargs.setdefault('on_delete', models.CASCADE)
        # because of makemigrations calling __init__ multiple times
        limit_to_model = kwargs.get('limit_to_model', None)
        kwargs.pop('limit_to_model', None)
        kwargs.setdefault('limit_choices_to', (self.form_choice_limit, [limit_to_model]))
        super().__init__(**kwargs)

    def get_limit_choices_to(self):
        """Allow the callable to have arguments, instead of the base django method"""
        if tuple(self.remote_field.limit_choices_to):
            return self.remote_field.limit_choices_to[0](*self.remote_field.limit_choices_to[1])
        else:
            return super().get_limit_choices_to()

    @staticmethod
    def form_choice_limit(name):
        """Limit the choice list displayed by the fields widget to template
        with the type matching the parent model"""
        return {'type': ContentType.objects.get(model=name)}

    def formfield(self, *, using=None, **kwargs):
        """Changes the default ForeignKey FormField to a custom one"""
        defaults = {'form_class': FormBuilderFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class DescriptorTemplate(models.Model):
    """Model for building forms from YAML Charfield"""
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Identifier"))
    type = models.ForeignKey(ContentType,
                             limit_choices_to=choice_limit,
                             on_delete=models.CASCADE, verbose_name=_("Type"))
    yaml_descriptor = models.TextField(verbose_name=_("Key value template"),
                                       help_text=_('Input as YAML'))

    def __str__(self):
        return self.slug

    def clean(self):
        """Check if it's valid YAML"""
        try:
            yaml.safe_load(self.yaml_descriptor)  # loads just basic tags
        except Exception as e:
            raise ValidationError(f'Not valid YAML: {e}')

    @property
    def descriptor_as_dict(self):
        """Converts the YAML field into dictionary"""
        return yaml.safe_load(self.yaml_descriptor)
