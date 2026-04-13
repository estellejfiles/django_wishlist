from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here

# create function to handle place_list url request
@login_required
def place_list(request):
    # check if method is POST method
    if request.method == 'POST':
        # create new place form from data sent in request
        form = NewPlaceForm(request.POST)
        # create model object from form
        place = form.save(commit=False)
        place.user = request.user
        # verify form is valid against db constraints
        if form.is_valid():
            # save form to db model
            place.save()
            # reloads home page
            return redirect('place_list')

    # gets places list from Place objects where visited=false & orders by name
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    # create new_place_form to create HTML
    new_place_form = NewPlaceForm()
    # return render request with data
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

# create function to handle visited page url request
@login_required
def places_visited(request):
    # database is queried for list of visited places
    visited = Place.objects.filter(visited=True)
    # return render request with data
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

# create function to handle request to set place as visited
@login_required
def place_was_visited(request, place_pk):
    # only execute on post methods
    if request.method == 'POST':
        # get place being updated by matching with place_pk; store in variable
        place = get_object_or_404(Place, pk=place_pk)
        # if place user matches request user, set place visited to true
        if place.user == request.user:
        # set place visited to true
            place.visited = True
            # save changes
            place.save()
        else:
            # if they do not match, return forbidden response
            return HttpResponseForbidden()
    # return redirect to wishlist visited places
    return redirect('places_visited')

# create function to handle place page url request
@login_required
def place_details(request, place_pk):
    # get place object
    place = get_object_or_404(Place, pk=place_pk)
    # return forbidden response if place does not belong to user
    if place.user != request.user:
        return HttpResponseForbidden()
    # check if post request
    if request.method == 'POST':
        # read form data by making new trip review form from request data
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # verify form is valid (all required fields are filled in and data is valid against db constraints)
        if form.is_valid():
            # save form to db model
            form.save()
            # show temporary message to user
            messages.info(request, 'Trip information updated!')
        else:
            # show temporary error message to user if form is not valid
            messages.error(request, form.errors)
        # return redirect to place details page
        return redirect('place_details', place_pk=place_pk)
    # execute else clause for get request
    else:
        # if place is visited show form using trip review form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        # if place is not visited, show place details without form
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})
    
# create function to handle delete place url request
@login_required
def delete_place(request, place_pk):
    # get place object
    place = get_object_or_404(Place, pk=place_pk)
    # if place user matches request user, delete place
    if place.user == request.user:
        place.delete()
        # return redirect to wishlist page
        return redirect('place_list')
    else:
        # if they do not match, return forbidden response
        return HttpResponseForbidden()

# create function to handle about page url request
def about(request):
    # create data to use as part of response
    author = 'Estelle'
    about = 'A website to create a list a list of places to visit'
    # return render request with data
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})