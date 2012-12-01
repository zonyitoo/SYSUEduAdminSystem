from django import forms

class ScoreUploadForm(forms.Form):
    file = forms.FileField()
