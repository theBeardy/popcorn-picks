from django import forms
from .models import Review

class MovieForm(forms.ModelForm):
    movie_title = forms.CharField(
        label="Movie Title", 
        max_length=255,
    )

    class Meta:
        model = Review
        exclude = ['user', 'movie_title']

    def clean(self):
        cleaned_data = super().clean()
        for field in ['visuals', 'acting', 'thought_provoking', 'dialog', 'makes_me_cry', 'genre_execution', 'rewatchability', 'fun_to_watch']:
            value = cleaned_data.get(field)
            if value is not None:
                cleaned_data[field] = max(1, min(value, 10))
        return cleaned_data

    # Optionally: to hide default model field so no conflict
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        i=0
        
        for field_name, field in self.fields.items():
            if field_name != 'movie_title':
                field.widget.attrs.update({
                    'class': 'font-default text-3xl text-center bg-light-4 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5 dark:bg-dark-4 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                })
            else:
                field.widget.attrs.update({
                    'class': 'font-default text-3xl text-center bg-light-4 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5 dark:bg-dark-4 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                })

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user','movie_title','average']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                    'class': 'font-default text-3xl text-center bg-light-4 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-2.5 dark:bg-dark-4 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
                })

class MovieFormModal(MovieForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'movie_title':
                field.widget.attrs.update({
                    "class": (
                        "h-8 w-[30%] ml-auto rounded-md "
                        "bg-light-4 dark:bg-dark-4 "
                        "px-2 text-3xl "
                        "focus:outline-none focus:ring-2 focus:ring-accent-light dark:focus:ring-accent-dark"
                    )
                })