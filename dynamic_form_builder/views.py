from django.http import HttpResponse

from dynamic_form_builder import models, forms
import json


def template_form_view(request, template_pk):
    """Send back a form rendered in HTML from a TemplateDescriptor instance"""
    inst = models.DescriptorTemplate.objects.get(pk=template_pk)

    form = forms.TemplateForm(inst.descriptor_as_dict)
    return HttpResponse(form.as_table())


class DynamicFormBuilderViewMixin:
    """Mixin to be used in CreateView and UpdateView"""

    def post(self, request, *args, **kwargs):
        """Retrieve the the dynamic form data"""
        self.dynamic_fields = {key.strip('jsonfield_'): value for key, value in request.POST.dict().items()
                               if key.startswith('jsonfield_')}
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Send back data as form"""
        ctx = super().get_context_data(**kwargs)
        if ctx.get('form', None):  # Create or Update views
            dyn_field = getattr(ctx['form'].instance, self.dynamic_field)
            if dyn_field:  # if data is already stored in the dyn_field
                ctx['json_form'] = forms.TemplateForm(json.loads(dyn_field))  # then displayed as form
            ctx['form'].fields.pop(self.dynamic_field)
        else:  # for detail views
            inst = kwargs['object']
            ctx['dyn_form_data'] = json.loads(getattr(inst, self.dynamic_field))
        return ctx

    def form_valid(self, form):
        """Store the dynamic form data into json"""
        setattr(form.instance, self.dynamic_field, json.dumps(self.dynamic_fields))
        return super().form_valid(form)
