from django import forms

class CommentForm(forms.Form):
    user = forms.CharField(label='Customer', max_length=10)
    email = forms.EmailField(label='E-Mail',max_length=20, required=False)
    content = forms.CharField(max_length=200, widget=forms.Textarea)

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 5:
            raise forms.ValidationError('the comment < 5')
        return content