from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'add_user', views.add_user),
    path(r'show_films', views.show_films),
]
