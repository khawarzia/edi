from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from random import shuffle as s1

def shuffle(a):
    b = []
    for i in range(len(a)):
        b.append(i)
    s1(b)
    c = []
    for i in b:
        c.append(a[i])
    return c

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

category_choice = (
    ('',''),
    ('Narrativa','Narrativa'),
    ('Erotico','Erotico'),
    ('Fiabe e Favole','Fiabe e Favole'),
    ('Horror','Horror'),
    ('Fantasy','Fantasy'),
    ('Sci-Fi','Sci-Fi'),
    ('Sentimenti','Sentimenti'),
    ('Umoristico','Umoristico'),
    ('Young Adult','Young Adult'),
    ('Blog','Blog'),
    ('Laboratorio di scrittura creativa','Laboratorio di scrittura creativa'),
    ('LibriCK scelti per Voi','LibriCK scelti per Voi'),
    ('Serie Top','Serie Top'),
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
    category = models.CharField(default='Narrativa',choices=category_choice,max_length=100)
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
    approved_by_admin_check_dont_change = models.BooleanField(default=False)
    check_for_points = models.BooleanField(default=False)

    def __str__(self):
        if self.approved_by_admin == False:
            return (self.status+' | Titled : '+self.title)
        else:
            return ('Approved'+' | Titled : '+self.title)
        
    def gettagslist(self):
        return self.tags.split(',')

class post_by_points(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(post , on_delete=models.CASCADE , blank=True)
    timestamp = models.IntegerField(default=0)

    def __str__(self):
        return (self.user.username)

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

class pointhistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    relpost = models.ManyToManyField(post)
    note = models.CharField(max_length=200,blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.note

class postgallery(models.Model):
    idtag = models.CharField(default='(([[(( idtag='+str(id)+' ))]]))',max_length=30)
    single_row = models.BooleanField(default=False)
    infinite_scroll = models.BooleanField(default=False)
    by_tag = models.BooleanField(default=False)
    by_category = models.BooleanField(default=False)
    by_date = models.BooleanField(default=False)
    tag1 = models.CharField(max_length=30,default='')
    tag2 = models.CharField(max_length=30,default='')
    tag3 = models.CharField(max_length=30,default='')
    tag4 = models.CharField(max_length=30,default='')
    tag5 = models.CharField(max_length=30,default='')
    category1 = models.CharField(default='',choices=category_choice,max_length=100)
    category2 = models.CharField(default='',choices=category_choice,max_length=100)
    category3 = models.CharField(default='',choices=category_choice,max_length=100)
    category4 = models.CharField(default='',choices=category_choice,max_length=100)
    category5 = models.CharField(default='',choices=category_choice,max_length=100)
    category6 = models.CharField(default='',choices=category_choice,max_length=100)
    category7 = models.CharField(default='',choices=category_choice,max_length=100)
    category8 = models.CharField(default='',choices=category_choice,max_length=100)
    category9 = models.CharField(default='',choices=category_choice,max_length=100)
    category10 = models.CharField(default='',choices=category_choice,max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.idtag

    def getproperties(self):
        objs = post.objects.filter(approved_by_admin=True)
        tagposts = []
        dateposts = []
        if self.by_category:
            if self.category1 != '':
                catposts = post.objects.filter(category=self.category1)
            else:
                catposts = []
            if self.category2 != '':
                c2 = post.objects.filter(category=self.category2)
                for i in c2:
                    if i not in catposts:
                        catposts.append(i)
            if self.category3 != '':
                c3 = post.objects.filter(category=self.category3)
                for i in c3:
                    if i not in catposts:
                        catposts.append(i)
            if self.category4 != '':
                c4 = post.objects.filter(category=self.category4)
                for i in c4:
                    if i not in catposts:
                        catposts.append(i)
            if self.category5 != '':
                c5 = post.objects.filter(category=self.category5)
                for i in c5:
                    if i not in catposts:
                        catposts.append(i)
            if self.category6 != '':
                c6 = post.objects.filter(category=self.category6)
                for i in c6:
                    if i not in catposts:
                        catposts.append(i)
            if self.category7 != '':
                c7 = post.objects.filter(category=self.category7)
                for i in c7:
                    if i not in catposts:
                        catposts.append(i)
            if self.category8 != '':
                c8 = post.objects.filter(category=self.category8)
                for i in c8:
                    if i not in catposts:
                        catposts.append(i)
            if self.category9 != '':
                c9 = post.objects.filter(category=self.category9)
                for i in c9:
                    if i not in catposts:
                        catposts.append(i)
            if self.category10 != '':
                c10 = post.objects.filter(category=self.category10)
                for i in c10:
                    if i not in catposts:
                        catposts.append(i)
        else:
            catposts = []
        
        if self.by_tag:
            for i in objs:
                if self.tag1 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag2 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag3 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag4 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag5 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
        else:
            tagposts = []

        if self.by_date:
            for i in objs:
                if i.post_date >= self.start_date and i.post_date <= self.end_date:
                    dateposts.append(i)
        else:
            dateposts = []

        if self.by_category and self.by_tag and self.by_date:
            allposts = list(set(catposts) & set(tagposts) & set(dateposts))
        elif self.by_date and self.by_category:
            allposts = list(set(catposts) & set(dateposts))
        elif self.by_date and self.by_tag:
            allposts = list(set(tagposts) & set(dateposts))
        elif self.by_tag and self.by_category:
            allposts = list(set(tagposts) & set(catposts))
        else:
            allposts = []

        return allposts

class postgalleryhome(models.Model):
    by_tag = models.BooleanField(default=False)
    by_category = models.BooleanField(default=False)
    by_date = models.BooleanField(default=False)
    tag1 = models.CharField(max_length=30,default='',blank=True)
    tag2 = models.CharField(max_length=30,default='',blank=True)
    tag3 = models.CharField(max_length=30,default='',blank=True)
    tag4 = models.CharField(max_length=30,default='',blank=True)
    tag5 = models.CharField(max_length=30,default='',blank=True)
    category1 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category2 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category3 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category4 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category5 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category6 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category7 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category8 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category9 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    category10 = models.CharField(default='',choices=category_choice,max_length=100,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return ('This is for home page only. Please make changes to this one only.')

    def getproperties(self):
        objs = post.objects.filter(approved_by_admin=True)
        tagposts = []
        dateposts = []
        if self.by_category:
            if self.category1 != '':
                catposts = post.objects.filter(category=self.category1)
            else:
                catposts = []
            if self.category2 != '':
                c2 = post.objects.filter(category=self.category2)
                for i in c2:
                    if i not in catposts:
                        catposts.append(i)
            if self.category3 != '':
                c3 = post.objects.filter(category=self.category3)
                for i in c3:
                    if i not in catposts:
                        catposts.append(i)
            if self.category4 != '':
                c4 = post.objects.filter(category=self.category4)
                for i in c4:
                    if i not in catposts:
                        catposts.append(i)
            if self.category5 != '':
                c5 = post.objects.filter(category=self.category5)
                for i in c5:
                    if i not in catposts:
                        catposts.append(i)
            if self.category6 != '':
                c6 = post.objects.filter(category=self.category6)
                for i in c6:
                    if i not in catposts:
                        catposts.append(i)
            if self.category7 != '':
                c7 = post.objects.filter(category=self.category7)
                for i in c7:
                    if i not in catposts:
                        catposts.append(i)
            if self.category8 != '':
                c8 = post.objects.filter(category=self.category8)
                for i in c8:
                    if i not in catposts:
                        catposts.append(i)
            if self.category9 != '':
                c9 = post.objects.filter(category=self.category9)
                for i in c9:
                    if i not in catposts:
                        catposts.append(i)
            if self.category10 != '':
                c10 = post.objects.filter(category=self.category10)
                for i in c10:
                    if i not in catposts:
                        catposts.append(i)
        else:
            catposts = []
        
        if self.by_tag:
            for i in objs:
                if self.tag1 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag2 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag3 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag4 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
                if self.tag5 in i.gettagslist:
                    if i not in tagposts:
                        tagposts.append(i)
        else:
            tagposts = []

        if self.by_date:
            for i in objs:
                if i.post_date >= self.start_date and i.post_date <= self.end_date:
                    dateposts.append(i)
        else:
            dateposts = []

        if self.by_category and self.by_tag and self.by_date:
            allposts = list(set(catposts) & set(tagposts) & set(dateposts))
        elif self.by_date and self.by_category:
            allposts = list(set(catposts) & set(dateposts))
        elif self.by_date and self.by_tag:
            allposts = list(set(tagposts) & set(dateposts))
        elif self.by_tag and self.by_category:
            allposts = list(set(tagposts) & set(catposts))
        elif self.by_category:
            allposts = catposts
        elif self.by_date:
            allposts = dateposts
        elif self.by_tag:
            allposts = tagposts
        else:
            allposts = []
        
        allposts = shuffle(allposts)
        
        allpostfinal = []
        for i in range(len(allposts)):
            a = {}
            a['id'] = i
            a['left'] = (i % 4) * 270
            a['cover'] = allposts[i].cover
            a['permalink'] = allposts[i].permalink
            a['title'] = allposts[i].title
            a['username'] = allposts[i].user.username
            if i > 3:
                a['show'] = 'none'
            else:
                a['show'] = 'block'
            allpostfinal.append(a)

        return allpostfinal