from django import forms


class PhotoForm(forms.Form):
    title = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        max_length=60,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    img = forms.ImageField()