from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, default="", blank=True, null=True)
    calendar_url = models.CharField(max_length=500, default="", blank=True, null=True)

    def __str__(self):
        return self.user.username