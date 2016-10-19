from django import forms

from .models import Video


class VideoModelForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = (
            'kind',
            'youtube_id',
            'title',
            'description',
            'published_date',
            'thumbnail_url',
        )
        widgets = {
            'kind': forms.HiddenInput(),
            'youtube_id': forms.HiddenInput(),
            'title': forms.HiddenInput(),
            'description': forms.HiddenInput(),
            'published_date': forms.HiddenInput(),
            'thumbnail_url': forms.HiddenInput(),
        }