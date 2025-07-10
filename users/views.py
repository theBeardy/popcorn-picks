from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, ExpressionWrapper, FloatField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from film_ratings.models import Movie, Review
from film_ratings.views import film_details

class TailwindAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'font-default bg-[var(--light-4)] dark:bg-[var(--dark-4)] mt-3 mb-2 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-[var(--dark-1)] dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            })

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("film_ratings:index")
    else:
        form = UserCreationForm()
    return render(request, "users/register_view.html", { 'form' : form })

def login_view(request):
    if request.method == "POST":
        form = TailwindAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("users:dashboard")
    else: 
        form = TailwindAuthenticationForm()
    return render(request, "users/login_view.html", { 'form' : form })

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("film_ratings:index")
    
@login_required(login_url='/users/login/')
def dashboard(request):
    # Manually average the 8 fields
    user_reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related('movie_title')
        .annotate(
            average_score=ExpressionWrapper(
                (
                    F('visuals') +
                    F('acting') +
                    F('thought_provoking') +
                    F('dialog') +
                    F('makes_me_cry') +
                    F('genre_execution') +
                    F('rewatchability') +
                    F('fun_to_watch')
                ) / 8.0,
                output_field=FloatField()
            )
        )
        .order_by('-average_score')
    )

    return render(request, "users/dashboard.html", {
        "user_review_data": user_reviews,
    })