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

selection_notification = (
    ('post','post'),
    ('comment','comment'),
    ('follow','follow'),
)

class follow(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = True , related_name='user')
    follower = models.ForeignKey(User , on_delete=models.CASCADE , blank = True , related_name='follower')

    def __str__(self):
        return (str(self.user.username)+' is followed by '+self.follower.username)

class post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , blank = True)
    title = models.TextField(max_length=200 , blank = True)
    permalink = models.CharField(max_length=100,blank=True)
    content = RichTextUploadingField(blank=True)
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
            return (self.status+' | Titled : '+self.title)
        else:
            return ('Approved'+' | Titled : '+self.title)

class comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    commentbody = RichTextField(blank = True)
    relpost = models.ManyToManyField(post,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (str(self.user)+' on '+str(self.relpost))

class comment_child(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    commentbody = RichTextField(blank=True)
    relcomment = models.ManyToManyField(comment,blank=True)
    relpost = models.ManyToManyField(post,blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.user)+' on '+str(self.relcomment))

class notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    relpost = models.ManyToManyField(post)
    relcom = models.ManyToManyField(comment)
    reluser = models.ManyToManyField(User,related_name='reluser')
    sel = models.CharField(blank=True,max_length=20,choices=selection_notification)
    notification = models.CharField(max_length=100,blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.notification