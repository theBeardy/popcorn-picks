from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from film_ratings.models import Movie, Review

class TailwindAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border bg-gray-100 border-gray-300 rounded px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'
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
    user_review_data = Review.objects.filter(user=request.user).select_related('movie_title')
    return render(request, 'users/dashboard.html', {"user_review_data": user_review_data})