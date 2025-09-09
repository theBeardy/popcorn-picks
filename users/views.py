from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, ExpressionWrapper, FloatField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from film_ratings.models import Movie, Review
from film_ratings.views import film_details

class TailwindAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'font-default w-[90%] bg-light-4 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-dark-4 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            })

class TailwindRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'font-default w-[90%] bg-light-4 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-dark-4 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            })

def register_view(request):
    if request.method == "POST":
        form = TailwindRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome 🎉")
            return redirect("film_ratings:index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TailwindRegistrationForm()
    return render(request, "users/register_view.html", { 'form' : form })

def login_view(request):
    if request.method == "POST":
        form = TailwindAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "You are now logged in ✅")
            redirect_to = request.POST.get("next") or request.GET.get("next") or "users:dashboard"
            return redirect(redirect_to)
        else: 
            messages.error(request, "Invalid username or password.")
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