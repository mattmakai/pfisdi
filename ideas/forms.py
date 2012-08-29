from django import forms
from ideas.models import Idea, ResearchLink

class IdeaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IdeaForm, self,).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'span12'
    class Meta:
        model = Idea
        exclude = ('owner', 'slug', 'tags', 'projects')


class ResearchLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResearchLinkForm, self,).__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs['class'] = 'span12'
    class Meta:
        model = ResearchLink
        exclude = ('owner', 'slug', 'tags')

