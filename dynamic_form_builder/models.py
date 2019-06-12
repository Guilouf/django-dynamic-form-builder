from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings

import yaml


def choice_limit():
    """Get the 'DYNAMIC_FORM_BUILDER_TARGETS' constant from the settings file to display
    models from the targeted app"""
    return {'app_label': getattr(settings, 'DYNAMIC_FORM_BUILDER_TARGET', None)}


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
