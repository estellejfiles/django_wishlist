from django import forms
from .models import Place

# create class for form to add new places for webpage related to model
class NewPlaceForm(forms.ModelForm):
    class Meta:
        # define model using Place
        model = Place
        # list model fields you want to be used (name and visited places)
        fields = ('name', 'visited')

# create class for form to input a date data type
# creating this allows a calendar widget to be used for user input convenience
class DateInput(forms.DateInput):
    input_type = 'date'

# create class for form to review visited places for webpage related to model
class TripReviewForm(forms.ModelForm):
    # create class Meta to describe info about the model
    class Meta:
        # define model using Place
        model = Place
        # list model fields to be used in form
        fields = ('notes', 'date_visited', 'photo')
        # create dictionary to specify widget for date_visited field
        widgets = {
            'date_visited': DateInput(),
        }