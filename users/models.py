from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_nick = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    localization = models.CharField(max_length=30)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s's profile" % self.user
