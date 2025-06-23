from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from film_ratings.models import Movie, Review

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("users:dashboard")
    else: 
        form = AuthenticationForm()
    return render(request, "users/login_view.html", { 'form' : form })

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("film_ratings:index")
    
@login_required(login_url='/users/login/')
def dashboard(request):
    user_review_data = Review.objects.filter(user=request.user).select_related('movie_title')
    return render(request, 'users/dashboard.html', {"user_review_data": user_review_data})