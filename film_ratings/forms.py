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

    def clean(self):
        cleaned_data = super().clean()
        for field in ['visuals', 'acting', 'thought_provoking', 'dialog', 'makes_me_cry', 'genre_execution', 'rewatchability', 'fun_to_watch']:
            value = cleaned_data.get(field)
            if value and value > 10:
                cleaned_data[field] = 10
        return cleaned_data

    # Optionally: to hide default model field so no conflict
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        i=0
        
        for field_name, field in self.fields.items():
            if field_name != 'movie_title':
                field.widget.attrs.update({
                    'class': 'font-default text-center bg-[var(--light-4)] text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-[var(--dark-4)] dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                })
            else:
                field.widget.attrs.update({
                    'class': 'font-default text-center bg-[var(--light-4)] text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-[var(--dark-4)] dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                })