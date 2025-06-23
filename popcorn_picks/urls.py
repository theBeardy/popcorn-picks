"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from film_ratings import views as film_ratings_views

urlpatterns = [
    path('', film_ratings_views.index, name="home"),
    path('film_ratings/', include(("film_ratings.urls", "film_ratings"), namespace="film_ratings")),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('admin/', admin.site.urls),
]
