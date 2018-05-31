from django import forms
from verity.models import RefereesMain, RefereesDetails

class RefereesMainForm(forms.ModelForm):
    actions = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = RefereesMain
        fields = ('__all__')


class RefereesDetailsForm(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea)
    main = forms.ModelChoiceField(
                queryset=RefereesMain.objects.all())
    class Meta:
        model = RefereesDetails
        fields = ('__all__')