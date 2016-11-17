from django import forms


class AlbumForm(forms.Form):
    title = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

