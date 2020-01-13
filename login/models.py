from django.db import models
from django.contrib.auth.models import User
from random import randint
from ckeditor.fields import RichTextField

class infor(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , blank = True)
    slug = models.SlugField(blank = True)
    passwordkey = models.CharField(max_length = 10 , blank = True)
    paypal_url = models.URLField(blank = True)
    choice = models.CharField(max_length = 20 , blank = True)
    cover = models.IntegerField(default = randint(1,23))
    cover_check = models.BooleanField(default = False)
    cover_img = models.ImageField(blank = True)
    profile = models.IntegerField(default = randint(1,2))
    profile_check = models.BooleanField(default = False)
    profile_pic = models.ImageField(blank = True)
    amazon_code_feature = RichTextField(blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return (str(self.user))

class temppic(models.Model):
    file = models.ImageField(blank = True)

class userpreferance(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE , blank = True)
    activity_mention = models.BooleanField(default = True)
    activity_response = models.BooleanField(default = True)
    message_recieve = models.BooleanField(default = True)
    followed = models.BooleanField(default = True)
    new_librick = models.BooleanField(default = True)

    def __str__(self):
        return (str(self.user))

class privacy_policy_and_terms_of_service(models.Model):
    privacy_policy = models.URLField(blank = True)
    terms_of_service = models.URLField(blank = True)