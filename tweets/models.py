from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    date = models.DateTimeField(auto_now_add=True)
    favs = models.IntegerField(default=0)

    def __str__(self):
        return self.text
