from django import forms

class RepoForm(forms.Form):
    repo_url = forms.URLField(label="Repository URL", required=True)
