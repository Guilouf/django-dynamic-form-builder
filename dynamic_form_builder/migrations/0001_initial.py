# Generated by Django 2.0.13 on 2019-06-12 11:57

from django.db import migrations, models
import django.db.models.deletion
import dynamic_form_builder.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptorTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Identifier')),
                ('yaml_descriptor', models.TextField(help_text='Input as YAML', verbose_name='Key value template')),
                ('type', models.ForeignKey(limit_choices_to=dynamic_form_builder.models.choice_limit, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='Type')),
            ],
        ),
    ]