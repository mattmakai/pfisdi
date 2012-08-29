from django import forms
from projects.models import Project

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'span12'

    class Meta:
        model = Project
        exclude = ('owner', 'slug', 'tags')
        
