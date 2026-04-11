from django.db import models
from django.contrib.auth.models import User

# create place model
class Place(models.Model):
    # initalize imported django user model as user attribute 
    # name the other table using a string, not allow ot be null, & specify what happens if user is deleted
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    # initalize Place name and visited attributes
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    # add notes attribute as text field that can be blank
    notes = models.TextField(blank=True, null=True)
    # add date visited attribute as date field that can be blank
    date_visited = models.DateField(blank=True, null=True)
    # add photo field that can be blank and upload image to user_images/
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        # photo_str refers to its url if it exists, otherwise it says 'no photo'
        photo_str = self.photo.url if self.photo else 'no photo'
        # store first 100 character of notes in notes_str, or say 'no notes' if there are none
        notes_str = self.notes[:100] + '...' if self.notes else 'no notes'
        return f'{self.name} visited? {self.visited} on {self.date_visited}. Notes: {notes_str} Photo: {photo_str}'