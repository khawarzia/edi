from django.db import models
from django.contrib.auth.models import User
from random import randint

class infor(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , null = True)
    slug = models.SlugField(null = True)
    passwordkey = models.CharField(max_length = 10 , null = True)
    paypal_url = models.URLField(null = True)
    choice = models.CharField(max_length = 20 , null = True)
    cover = models.IntegerField(default = randint(1,23))
    cover_check = models.BooleanField(default = False)
    cover_img = models.ImageField(null = True)
    profile = models.IntegerField(default = randint(1,2))
    profile_check = models.BooleanField(default = False)
    profile_pic = models.ImageField(null = True)

    def __str__(self):
        return (str(self.user))

class temppic(models.Model):
    file = models.ImageField(null = True)

class userpreferance(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , null = True)
    activity_mention = models.BooleanField(default = True)
    activity_response = models.BooleanField(default = True)
    message_recieve = models.BooleanField(default = True)
    followed = models.BooleanField(default = True)
    new_librick = models.BooleanField(default = True)

    def __str__(self):
        return (str(self.user))

class privacy_policy_and_terms_of_service(models.Model):
    privacy_policy = models.URLField(null = True)
    terms_of_service = models.URLField(null = True)