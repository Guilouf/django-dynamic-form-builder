from django.http import HttpResponse

from dynamic_form_builder import models, forms


def template_form_view(request, template_pk):
    """Send back a form rendered in HTML from a TemplateDescriptor instance"""
    inst = models.DescriptorTemplate.objects.get(pk=template_pk)

    form = forms.TemplateForm(inst.descriptor_as_dict)
    return HttpResponse(form.as_table())
