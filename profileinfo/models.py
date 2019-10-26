from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

status_choice = (
    ('draft','draft'),
    ('processing','processing'),
)

type_choice = (
    ('single post','single post'),
    ('post part of series','post part of series'),
)

class follow(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = True)
    follower = models.CharField(max_length = 50 , blank = True)

    def __str__(self):
        return (str(self.user)+' is followed by '+self.follower)

class post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = True)
    title = RichTextField(unique=True,config_name = 'special')
    titledisplay = models.CharField(max_length=100,blank=True)
    content = RichTextUploadingField(blank=True)
    contentdisplay = models.CharField(max_length=250,blank=True)
    tags = models.CharField(max_length=200,blank=True)
    cover = models.ImageField(blank=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User , related_name='likes',blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(blank=True,max_length=20,choices=status_choice)
    type_of_post = models.CharField(blank=True,max_length=40,choices=type_choice)
    linked_checked = models.BooleanField(default=False)
    linked_post = models.ManyToManyField('profileinfo.post',blank=True)
    link_number = models.IntegerField(default=1)
    link_title = models.CharField(blank=True,max_length=100)
    approved_by_admin = models.BooleanField(default=False)

    def __str__(self):
        if self.approved_by_admin == False:
            return (self.status)
        if self.approved_by_admin:
            return ('Approved')
        return (self.titledisplay)

class comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    commentbody = RichTextField(blank = True)
    commentbodydisplay = models.CharField(max_length=500,blank=True)
    relpost = models.ManyToManyField(post,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (str(self.user)+' on '+str(self.relpost))

class comment_child(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    commentbody = RichTextField(blank=True)
    commentbodydisplay = models.CharField(max_length=500,blank=True)
    relcomment = models.ManyToManyField(comment,blank=True)
    relpost = models.ManyToManyField(post,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.user)+' on '+str(self.relcomment))

class message(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE ,related_name='sender', blank = True)
    reciever = models.ManyToManyField(User ,related_name='reciever', blank = True)
    message = models.CharField(max_length = 500 , blank = True)
    sentdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 10, blank = True)

    def __str__(self):
        return ()

class notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    relpost = models.ManyToManyField(post)
    notification = models.CharField(max_length=100,blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.notification