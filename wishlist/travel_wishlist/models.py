from django.db import models

# create place model
class Place(models.Model):
    # initalize Place name and visited attributes
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} visited? {self.visited}'