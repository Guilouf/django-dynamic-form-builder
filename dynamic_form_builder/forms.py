from django import forms


class TemplateForm(forms.Form):
    """Form that builds it up from a dictionary"""

    def __init__(self, fields):
        super().__init__()
        for fieldname, value in fields.items():
            # fields inputs are prefixed to be filtered out when posted
            self.fields[f"jsonfield_{fieldname}"] = forms.CharField(label=fieldname, initial=value)
