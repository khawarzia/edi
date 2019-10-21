from django.shortcuts import render,redirect,HttpResponse
from .models import follow,post,message,comment,comment_child,notifications
from login.models import infor,privacy_policy_and_terms_of_service,userpreferance
from django.contrib.auth.decorators import login_required
from random import randint
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from fblogin.settings import DEBUG
from login.forms import PhotoForm1,PhotoForm2
from django.core.files.storage import FileSystemStorage
from html2text import html2text
import operator
from django.core.mail import EmailMessage
from .forms import contentform

def info(request):
    obj = infor.objects.get(user=request.user)
    if obj.cover_check:
        coverimg = "a"
    else:
        coverimg = "b"
    if obj.profile_check == False:
        try:
            a = request.user.socialaccount_set.all()[0].provider
            profileimg = "b"
        except:
            profileimg = "c"
    else:
        profileimg = "a"
    objs = follow.objects.all()
    followers = 0
    following = 0
    for i in objs:
        if i.user == request.user:
            followers += 1
        if i.follower == request.user:
            following += 1
    objs = post.objects.all()
    posts = 0
    for i in objs:
        if i.user == request.user and i.approved_by_admin:
            posts += 1
    objs = message.objects.all()
    messages = 0
    for i in objs:
        if i.reciever == request.user:
            messages += 1
    notifi = 0
    notific = []
    objs = notifications.objects.all()
    for i in objs:
        if i.user == request.user and i.status == False:
            notifi += 1
            notific.append(i)
    context = {'infor':obj,'user_check':True,'coverurl':coverimg,'profileurl':profileimg,'notific':notific,'notifications':notifi,'followers':followers,'following':following,'posts':posts,'messages':messages,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
    return context

def profile_page(request,the_slug):
    context = {'followers':0,'following':0,'posts':0,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
    if request.user.is_authenticated:
        template = 'profile.html'
        context = info(request)
        if request.user != infor.objects.get(slug = the_slug).user:
            context['user_check'] = False
            context['infor2'] = infor.objects.get(slug = the_slug)
            a = User.objects.all()
            for i in a:
                if i == context['infor2'].user:
                    context['user2'] = i
            obj = context['infor2']
            if obj.cover_check:
                coverimg = "a"
            else:
                coverimg = "b"
            if obj.profile_check == False:
                try:
                    a = context['user2'].socialaccount_set.all()[0].provider
                    profileimg = "b"
                except:
                    profileimg = "c"
            else:
                profileimg = "a"
            context['coverurl2'] = coverimg
            context['profileurl2'] = profileimg
    else:
        template = 'profile-no.html'
        context['user_check'] = False
        context['infor2'] = infor.objects.get(slug = the_slug)
        a = User.objects.all()
        for i in a:
            if i == context['infor2'].user:
                context['user2'] = i
        obj = context['infor2']
        if obj.cover_check:
            coverimg = "a"
        else:
            coverimg = "b"
        if obj.profile_check == False:
            try:
                a = context['user2'].socialaccount_set.all()[0].provider
                profileimg = "b"
            except:
                profileimg = "c"
        else:
            profileimg = "a"
        context['coverurl2'] = coverimg
        context['profileurl2'] = profileimg
    objs = post.objects.all()
    a = []
    for i in objs:
        if i.user.username == the_slug and i.approved_by_admin == True:
            a.append(i)
            i.titledisplay = html2text(i.title)
            i.contentdisplay = html2text(i.content)[0:100]
            i.save()
    context['postdata'] = a
    return render(request,template,context)

@login_required(login_url='/loggin')
def drafts(request):
    template = 'profile-drafts.html'
    context = info(request)
    objs = post.objects.all()
    a = []
    for i in objs:
        if i.user == request.user and (i.status == 'draft' and i.approved_by_admin == False):
            a.append(i)
    context['postdata'] = a
    return render(request,template,context)

@login_required(login_url = '/loggin')
def insospeso(request):
    template = 'profile-insospeso.html'
    context = info(request)
    objs = post.objects.all()
    a = []
    for i in objs:
        if i.user == request.user and i.status == 'processing' and i.approved_by_admin == False:
            a.append(i)
    context['postdata'] = a
    return render(request,template,context)

@login_required(login_url = '/loggin')
def randomcover(request):
    a = infor.objects.get(user=request.user)
    a.cover = randint(1,23)
    a.cover_check = False
    a.save()
    return redirect('/membri/'+str(request.user.username))

def viewprofile(request,the_slug):
    context = {'followers':0,'following':0,'posts':0,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
    if request.user.is_authenticated:
        template = 'profileview.html'
        context = info(request)
        if request.user != infor.objects.get(slug = the_slug).user:
            context['user_check'] = False
            context['infor2'] = infor.objects.get(slug = the_slug)
            a = User.objects.all()
            for i in a:
                if i == context['infor2'].user:
                    context['user2'] = i
            obj = context['infor2']
            if obj.cover_check:
                coverimg = "a"
            else:
                coverimg = "b"
            if obj.profile_check == False:
                try:
                    a = context['user2'].socialaccount_set.all()[0].provider
                    profileimg = "b"
                except:
                    profileimg = "c"
            else:
                profileimg = "a"
            context['coverurl2'] = coverimg
            context['profileurl2'] = profileimg
    else:
        template = 'profile-no-profile.html'
        context['user_check'] = False
        context['infor2'] = infor.objects.get(slug = the_slug)
        a = User.objects.all()
        for i in a:
            if i == context['infor2'].user:
                context['user2'] = i
        obj = context['infor2']
        if obj.cover_check:
            coverimg = "a"
        else:
            coverimg = "b"
        if obj.profile_check == False:
            try:
                a = context['user2'].socialaccount_set.all()[0].provider
                profileimg = "b"
            except:
                profileimg = "c"
        else:
            profileimg = "a"
        context['coverurl2'] = coverimg
        context['profileurl2'] = profileimg        
    return render(request,template,context)

@login_required(login_url='/loggin')
def editprofile(request):
    template = 'profileedit.html'
    context = info(request)
    if request.method == 'POST':
        a = request.POST['field_1']
        obj = request.user
        obj.first_name = a
        obj.last_name = ''
        obj.save()
        b = request.POST['field_140']
        obj = context['infor']
        obj.paypal_url = b
        obj.save()
        context = info(request)
    return render(request,template,context)

@login_required(login_url='/loggin')
def editprofilepic(request):
    template = 'profilepicedit.html'
    context = info(request)
    form = PhotoForm2(request.POST, request.FILES)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            form.save(request.user)
            return redirect('/editprofilepic')
        context = info(request)
    return render(request,template,context)

@login_required(login_url='/loggin')
def editprofilecover(request):
    template = 'coverpicedit.html'
    context = info(request)
    form = PhotoForm1(request.POST, request.FILES)
    context['form'] = form
    if request.method == 'POST':
        if form.is_valid():
            form.save(request.user)
            return redirect('/editprofilecover')
        context = info(request)
    return render(request,template,context)

@login_required(login_url = '/loggin')
def deleteprofilepic(request):
    obj = infor.objects.get(user = request.user)
    obj.profile_pic = None
    obj.save()
    return redirect('/editprofilepic')

@login_required(login_url = '/loggin')
def deletecoverpic(request):
    obj = infor.objects.get(user = request.user)
    obj.cover = 0
    obj.cover_check = False
    obj.save()
    return redirect('/editprofilecover')

@login_required(login_url='/loggin')
def settingsgeneral(request):
    template = 'settingsgeneral.html'
    context = info(request)
    if request.method == 'POST':
        a = request.POST['pwd']
        b = request.POST['email']
        c = request.POST['pass1']
        d = request.POST['pass2']
        obj = User.objects.get(username = request.user.username)
        if obj.check_password(a):
            obj.email = b
            obj.save()
            if c == d and c != '':
                print('a')
                obj.set_password(c)
                obj.save()
        context = info(request)
        return render(request,template,context)
    return render(request,template,context)

@login_required(login_url='/loggin')
def settingsemail(request):
    template = 'settingsemail.html'
    context = info(request)
    a = []
    obj = userpreferance.objects.get(user = request.user)
    a.append(obj.activity_mention)
    a.append(obj.activity_response)
    a.append(obj.message_recieve)
    a.append(obj.followed)
    a.append(obj.new_librick)
    context['a'] = a
    print (a)
    if request.method == "POST":
        a = ['','','','','']
        b = []
        valbool = False
        a[0] = request.POST['notifications[notification_activity_new_mention]']
        a[1] = request.POST['notifications[notification_activity_new_reply]']
        a[2] = request.POST['notifications[notification_messages_new_message]']
        a[3] = request.POST['notifications[notification_starts_following]']
        a[4] = request.POST['notifications[notification_leader_publishes_post]']
        for i in a:
            if i == 'yes':
                valbool = True
            else:
                valbool = False
            b.append(valbool)
        obj = userpreferance.objects.get(user = request.user)
        obj.activity_mention = b[0]
        obj.activity_response = b[1]
        obj.message_recieve = b[2]
        obj.followed = b[3]
        obj.new_librick = b[4]
        obj.save()
        context['a'] = b
        print (b)
    return render(request,template,context)

@login_required(login_url='/loggin')
def settingscancel(request):
    template = 'settingscancel.html'
    context = info(request)
    return render(request,template,context)

@login_required(login_url='/loggin')
def deleteaccount(request):
    a = User.objects.get(username = request.user.username)
    a.delete()
    return redirect('/')

@login_required(login_url='/loggin')
def notification_read(request):
    template = 'notification-read.html'
    context = info(request)
    objs = notifications.objects.all()
    a = []
    for i in objs:
        if i.status:
            a.append(i)
    context['notifi'] = a
    return render(request,template,context)

@login_required(login_url='/loggin')
def notification_unread(request):
    template = 'notification-unread.html'
    context = info(request)
    objs = notifications.objects.all()
    a = []
    for i in objs:
        if not i.status:
            a.append(i)
            i.status = True
            i.save()
    context['notifi'] = a
    return render(request,template,context)

@login_required(login_url='/loggin')
def new_post(request):
    template = 'new-post.html'
    context = info(request)
    a = []
    try:
        posts = post.objects.all()
        for i in posts:
            if i.type_of_post == 'post part of series' and i.user == request.user:
                if i.link_number == 1 and i.linked_post.all().count() < 9:
                    a.append(i.link_title)
    except:
        pass
    context['series'] = a
    if request.method == 'POST':
        form = contentform(request.POST)
        postdata = request.POST
        a = post()
        a.user = request.user
        a.title = postdata['title']
        if form.is_valid():
            a.content = form.cleaned_data['content']
        else:
            a.content = ''
        a.tags = str(postdata['tags'])
        try:
            image = request.FILES['coverimg']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            a.cover = fs.url(filename)
        except:
            a.cover = ''
        if postdata['action'] == '':
            a.status = 'processing'
        else:
            a.status = 'draft'
        try:
            seriname = postdata['_new_serie']
        except:
            seriname = ''
        try:
            seri = postdata['post_serie']
        except:
            seri = ''
        try:
            typ = postdata['post_type']
        except:
            typ = ''
        if typ == '':
            a.type_of_post = 'single post'
        elif typ == 'new-serie':
            a.type_of_post = 'post part of series'
            a.link_title = seriname
            a.linked_checked = True
        else:
            a.type_of_post = 'post part of series'
            a.link_title = seri
            a.linked_checked = True            
            objs = post.objects.all()
            count = 1
            for i in objs:
                if i.user == request.user and i.link_title == seri:
                    a.save()
                    i.linked_post.add(a)
                    i.save()
                    epi = i.linked_post.all()
                    for j in epi:
                        a.linked_post.add(j)
                    count += 1
            a.link_number = count
        a.titledisplay = html2text(a.title)
        a.contentdisplay = html2text(a.content)[0:250]
        a.save()
        return redirect('/membri/'+str(request.user.username))
    else:
        form = contentform()
    context['form'] = form
    return render(request,template,context)

def view_post(request,title):
    context = {}
    if request.user.is_authenticated:
        template = 'view-post.html'
        context = info(request)
    else:
        template = 'view-post-no.html'
    objs = post.objects.all()
    for i in objs:
        if i.titledisplay == title:
            obj = i
            i.views += 1
            i.save()
            break
    try:
        print(obj.title)
    except:
        return redirect('/')
    commentdata = {}
    objs = comment.objects.all()
    objs2 = comment_child.objects.all()
    for i in objs:
        if i.relpost.all()[0] == obj:
            commentdata[i] = {}
            inforobj = infor.objects.get(user=i.user)
            if inforobj.profile_check == False:
                try:
                    a = i.user.socialaccount_set.all()[0].provider
                    profileimg = "b"
                except:
                    profileimg = "c"
            else:
                profileimg = "a"
            commentdata[i]['pf'] = profileimg
            commentdata[i]['cominfor'] = inforobj
            commentdata[i]['number'] = len(commentdata)
            commentdata[i]['children'] = {}
            for j in objs2:
                if j.relcomment.all()[0] == i and j.relpost.all()[0] == i.relpost.all()[0]:
                    commentdata[i]['children'][j] = {}
                    inforobj = infor.objects.get(user=j.user)
                    if inforobj.profile_check == False:
                        try:
                            a = j.user.socialaccount_set.all()[0].provider
                            profileimg = "b"
                        except:
                            profileimg = "c"
                    else:
                        profileimg = "a"                    
                    commentdata[i]['children'][j]['pf'] = profileimg
                    commentdata[i]['children'][j]['cominfor'] = inforobj
    inforobj = infor.objects.get(user = obj.user)
    if inforobj.profile_check == False:
        try:
            a = obj.user.socialaccount_set.all()[0].provider
            profileimg = "b"
        except:
            profileimg = "c"
    else:
        profileimg = "a"
    episodes = []
    for i in obj.linked_post.all():
        a = {}
        a['number'] = i.link_number
        a['titled'] = i.titledisplay
        if obj.link_number != i.link_number:
            a['check'] = False
        else:
            a['check'] = True
        episodes.append(a)
    episodes.sort(key=operator.itemgetter('number'))
    print (episodes)
    context['epilist'] = episodes
    context['postprofileurl'] = profileimg
    context['post'] = obj
    context['postinfor'] = inforobj
    context['cd'] = commentdata.items()
    print (commentdata.items())
    return render(request,template,context)

@login_required(login_url='/loggin')
def comment_new(request,title):
    if request.method == 'POST':
        a = request.POST['comment']
        obj = comment()
        obj.user = request.user
        obj.commentbody = a
        obj.commentbodydisplay = html2text(a)
        obj.save()
        obj.relpost.add(post.objects.get(titledisplay = title)) 
        obj.save()
        obj2 = notifications()
        obj2.user = obj.relpost.all()[0].user
        obj2.save()
        obj2.relpost.add(obj.relpost.all()[0])
        obj2.notification = str(obj.user.username)+' ha commentato '+str(title)
        obj2.save()
        a = EmailMessage(
            subject='Commento',
            body=str(title)+' e stato commentato : '+str(obj.commentbodydisplay)+' https://67.207.92.234:8000/post/'+title+ ' https://67.207.92.234:8000/notifications-unread',
            to=[obj2.user.email]
        )
        a.send()
        return redirect('/post/'+title)
    
@login_required(login_url='/loggin')
def new_child(request,title,body):
    if request.method == 'POST':
        a = request.POST['comment']
        obj = comment_child()
        obj.user = request.user
        obj.commentbody = a
        obj.commentbodydisplay = html2text(a)
        obj.save()
        obj.relpost.add(post.objects.get(titledisplay = title))
        obj.relcomment.add(comment.objects.get(commentbodydisplay = body))
        obj.save()
        return redirect('/post/'+title)

@login_required(login_url='/loggin')
def like_post(request,title):
    obj = post.objects.get(titledisplay = title)
    objs = obj.likes.all()
    if request.user in objs:
        obj.likes.remove(request.user)
        obj.save()
        return redirect('/post/'+title)
    else:
        obj.likes.add(request.user)
        obj.save()
        return redirect('/post/'+title)

@login_required(login_url='/loggin')
def edit_post(request,title):
    template = 'new-post.html'
    context = info(request)
    obj = post.objects.get(titledisplay = title)
    if obj.user == request.user:
        pass
    else:
        return redirect('/')
    context['post'] = obj
    context['poststatus'] = True
    a = []
    try:
        posts = post.objects.all()
        for i in posts:
            if i.type_of_post == 'post part of series' and i.user == request.user:
                if i.link_number == 1 and i.linked_post.all().count() < 9:
                    a.append(i.link_title)
    except:
        pass
    context['series'] = a
    if request.method == 'POST':
        form = contentform(request.POST)
        postdata = request.POST
        a = obj
        a.title = postdata['title']
        a.content = form.cleaned_data['content']
        a.tags = str(postdata['tags'])
        image = request.FILES['coverimg']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        a.cover = fs.url(filename)
        if postdata['action'] == '':
            a.status = 'processing'
        else:
            a.status = 'draft'
        try:
            typ = postdata['post_type']
            seriname = postdata['_new_serie']
            seri = postdata['post_serie']
        except:
            typ = ''
            seriname = ''
            seri = ''
        if typ == '':
            a.type_of_post = 'single post'
        elif typ == 'new-serie':
            a.type_of_post = 'post part of series'
            a.link_title = seriname
        else:
            a.type_of_post = 'post part of series'
            a.link_title = seri            
            objs = post.objects.all()
            count = 1
            for i in objs:
                if i.user == request.user and i.link_title == seri:
                    a.save()
                    i.linked_post.add(a)
                    i.save()
                    epi = i.linked_post.all()
                    for j in epi:
                        a.linked_post.add(j)
                    count += 1
            a.link_number = count
        a.titledisplay = html2text(a.title)
        a.contentdisplay = html2text(a.content)[0:250]
        a.save()
        return redirect('/membri/'+str(request.user.username))
    else:
        form = contentform(instance=obj)
    context['form'] = form
    return render(request,template,context)

@login_required(login_url='/loggin')
def preview_post(request):
    template = 'post-preview.html'
    context = info(request)
    if request.method == 'POST':
        print (request.POST)
        try:
            image = request.FILES['coverimg']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            context['coverimg'] = fs.url(filename)
        except:
            context['coverimg'] = ''
        context['main_body'] = request.POST['main-body']
        context['post'] = request.POST
    return render(request,template,context)
