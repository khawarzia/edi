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
    user = models.ForeignKey(User , on_delete=models.CASCADE , null = True)
    follower = models.CharField(max_length = 50 , null = True)

    def __str__(self):
        return (str(self.user)+' is followed by '+self.follower)

class post(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , null = True)
    title = RichTextField(unique=True,config_name = 'special')
    titledisplay = models.CharField(max_length=100,null=True)
    content = RichTextUploadingField(null=True)
    contentdisplay = models.CharField(max_length=30,null=True)
    amazon_code_feature = RichTextField(blank=True)
    tags = models.CharField(max_length=200,null=True)
    cover = models.ImageField(null=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User , related_name='likes')
    post_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True,max_length=20,choices=status_choice)
    type_of_post = models.CharField(null=True,max_length=40,choices=type_choice)
    linked_checked = models.BooleanField(default=False)
    linked_post = models.ManyToManyField('profileinfo.post')
    link_number = models.IntegerField(default=1)
    link_title = models.CharField(null=True,max_length=100)
    approved_by_admin = models.BooleanField(default=False)

    def __str__(self):
        if self.status == 'processing' and self.approved_by_admin == False:
            return ('Waiting for approval')
        if self.approved_by_admin:
            return ('Approved')
        return (str(self.titledisplay)+' by '+str(self.user)+' status : '+self.status )

class comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    commentbody = RichTextField(null = True)
    commentbodydisplay = models.CharField(max_length=500,null=True)
    relpost = models.ManyToManyField(post,null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (str(self.user)+' on '+str(self.relpost))

class comment_child(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    commentbody = RichTextField(null=True)
    commentbodydisplay = models.CharField(max_length=500,null=True)
    relcomment = models.ManyToManyField(comment,null=True)
    relpost = models.ManyToManyField(post,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (str(self.user)+' on '+str(self.relcomment))

class message(models.Model):
    sender = models.ForeignKey(User , on_delete=models.CASCADE ,related_name='sender', null = True)
    reciever = models.ManyToManyField(User ,related_name='reciever', null = True)
    message = models.CharField(max_length = 500 , null = True)
    sentdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 10, null = True)

    def __str__(self):
        return ()

class notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    relpost = models.ManyToManyField(post)
    notification = models.CharField(max_length=100,null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.notification