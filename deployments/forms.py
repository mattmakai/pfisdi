from django import forms
from deployments.models import Deployment

class AssociateDeploymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssociateDeploymentForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'span12'
    class Meta:
        model = Deployment 
        exclude = ('owner','slug')
