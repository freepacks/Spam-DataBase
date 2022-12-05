from django import forms

class Mail(forms.Form):
   mail = forms.CharField(
    widget=forms.Textarea(attrs={"rows":"5"}),
    label='')