from django import forms
from .models import Place

# create class for form for webpage related to model
class NewPlaceForm(forms.ModelForm):
    class Meta:
        # define model using Place
        model = Place
        # list model fields you want to be used (name and visited places)
        fields = ('name', 'visited')