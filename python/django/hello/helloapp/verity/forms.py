from django import forms
from verity.models import RefereesMain

class RefereesMainForm(forms.ModelForm):
    actions = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = RefereesMain
        fields = ('__all__')