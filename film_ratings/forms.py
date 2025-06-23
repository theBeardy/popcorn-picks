from django import forms
from .models import Review

class MovieForm(forms.ModelForm):
    movie_title = forms.CharField(label="Movie Title", max_length=255)

    class Meta:
        model = Review
        exclude = ['movie_title', 'user', 'movie_title']

    # Optionally: to hide default model field so no conflict
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'movie_title' in self.fields:
            self.fields['movie_title'].widget.attrs.update({'placeholder': 'Start typing a movie title...'})