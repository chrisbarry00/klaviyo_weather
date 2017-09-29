from django.db import models
from cities.models import City


class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    city = models.ForeignKey(City, blank=True, null=True)

    def __str__(self):
        return self.email
