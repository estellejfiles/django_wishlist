from django.urls import path
from . import views

urlpatterns = [
    # state url path for homepage ('')
    path('', views.place_list, name='place_list'),
    # state url path for visited request
    path('visited', views.places_visited, name='places_visited'),
    # state url path for setting a place as visited
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    # state url path for about page
    path('about', views.about, name='about')
]