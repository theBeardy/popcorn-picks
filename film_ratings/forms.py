from django import forms
from .models import Review

class MovieForm(forms.ModelForm):
    movie_title = forms.CharField(
        label="Movie Title", 
        max_length=255,
    )

    class Meta:
        model = Review
        exclude = ['movie_title', 'user', 'movie_title']

    # Optionally: to hide default model field so no conflict
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        i=0
        
        for field_name, field in self.fields.items():
            if field_name != 'movie_title':
                field.widget.attrs.update({
                    'class': 'text-center bg-[#354F52] text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-[#354F52] dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full text-center px-4 py-2 bg-white border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500'
                })