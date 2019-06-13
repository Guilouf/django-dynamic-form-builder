from django import template

register = template.Library()


@register.inclusion_tag('dynamic_form_builder/table_form.html')
def overridable_table_form(form):
    """Adds a form in a table section that have a special id to eventually overrided"""
    return {'form': form}
