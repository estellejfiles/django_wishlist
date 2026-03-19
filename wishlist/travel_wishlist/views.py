from django.shortcuts import render, redirect
from .models import Place
from .forms import NewPlaceForm

# Create your views here

# create function to handle place_list url request
def place_list(request):
    # check if method is POST method
    if request.method == 'POST':
        # create new place form from data sent in request
        form = NewPlaceForm(request.POST)
        # create model object from form
        place = form.save()
        # verify form is valid against db constraints
        if form.is_valid():
            # save form to db model
            place.save()
            # reloads home page
            return redirect('place_list')

    # gets places list from Place objects where visited=fale & orders by name
    places = Place.objects.filter(visited=False).order_by('name')
    # create new_place_form to create HTML
    new_place_form = NewPlaceForm()
    # return render request with data
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

# create function to handle visited page url request
def places_visited(request):
    # get list of visited places
    visited = Place.objects.filter(visited=True)
    # return render request with data
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })
# create function to handle about page url request

def about(request):
    # create data to use as part of response
    author = 'Estelle'
    about = 'A website to create a list a list of places to visit'
    # return render request with data
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})