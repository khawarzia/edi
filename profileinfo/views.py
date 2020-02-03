from django.shortcuts import render,redirect,HttpResponse
from .models import follow,post,comment,comment_child,notifications,pointhistory,post_by_points
from chat.models import Message as message
from login.models import infor,privacy_policy_and_terms_of_service,userpreferance
from django.contrib.auth.decorators import login_required
from random import randint
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from fblogin.settings import DEBUG
from login.forms import PhotoForm1,PhotoForm2
from django.core.files.storage import FileSystemStorage
import operator
from django.core.mail import EmailMessage
from .forms import contentform,titleform
from html2text import html2text
from django.http.response import JsonResponse
import time

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
    followinglist = []
    for i in objs:
        if i.user == request.user:
            followers += 1
        if i.follower == request.user:
            followinglist.append(i.user)
            following += 1
    objs = post.objects.all()
    posts = 0
    for i in objs:
        if i.user == request.user and i.approved_by_admin:
            posts += 1
    objs = message.objects.all()
    messages = 0
    for i in objs:
        if i.receiver == request.user:
            messages += 1
    notifi = 0
    notific = []
    objs = notifications.objects.all()
    for i in objs:
        if i.user == request.user and i.status == False:
            notifi += 1
            notific.append(i)
    notific.reverse()
    context = {'infor':obj,'user_check':True,'coverurl':coverimg,'profileurl':profileimg,'notific':notific,
                'notifications':notifi,'followers':followers,'following':following,'posts':posts,'messages':messages,
                'followinglist':followinglist,
                'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
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
            context['followcheck'] = False
            objs = follow.objects.all()
            for i in objs:
                if i.follower == request.user and i.user == context['user2']:
                    context['followcheck'] = True
                    break
            followers = 0
            following = 0
            for i in objs:
                if i.user == context['user2']:
                    followers += 1
                if i.follower == context['user2']:
                    following += 1
            context['followers'] = followers
            context['following'] = following
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
    context['postdata'] = a
    context['posts'] = len(a)
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
        if i.status and i.user == request.user:
            a.append(i)
    a.reverse()
    context['notifi'] = a
    return render(request,template,context)

@login_required(login_url='/loggin')
def notification_unread(request):
    template = 'notification-unread.html'
    context = info(request)
    objs = notifications.objects.all()
    a = []
    for i in objs:
        if not i.status and i.user == request.user:
            a.append(i)
            i.status = True
            i.save()
    a.reverse()
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
                if i.link_number == 1 and i.linked_post.count() < 10:
                    if i.link_title not in a:
                        a.append(i.link_title)
    except:
        pass
    context['series'] = a
    if request.method == 'POST':
        form = contentform(request.POST)
        form2 = titleform(request.POST)
        postdata = request.POST
        a = post()
        a.user = request.user
        if form2.is_valid():
            a.title = html2text(form2.cleaned_data['title'])
            if a.title == '':
                return redirect('/invia-un-racconto')
        else:
            return redirect('/invia-un-racconto')
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
            a.save()
            a.linked_post.add(a)
        else:
            a.type_of_post = 'post part of series'
            a.link_title = seri
            a.linked_checked = True            
            objs = post.objects.all()
            a.save()
            for i in objs:
                if i.user == request.user and i.link_title == seri:
                    i.linked_post.add(a)
                    i.save()
                    a.linked_post.add(i)
            a.link_number = a.linked_post.count()
        a.permalink = convertit(a.title)
        a.save()
        objs = post.objects.all()
        return redirect('/edit/'+a.permalink)
    else:
        form = contentform()
        form2 = titleform()
    context['form'] = form
    context['form2'] = form2
    return render(request,template,context)

def view_post(request,title):
    totallength = 0
    context = {}
    if request.user.is_authenticated:
        template = 'view-post.html'
    else:
        template = 'view-post-no.html'
    checkp = 1
    objs = post.objects.all()
    for i in objs:
        if i.permalink == title:
            obj = i
            if obj.check_for_points:
                if request.user.is_authenticated:
                    pointobjs = post_by_points.objects.filter(user=request.user)
                    for j in pointobjs:
                        if j.post == obj:
                            if (time.time() - j.timestamp) <= 86400:
                                checkp = 0
                                break
                            else:
                                checkp = 1
                                j.delete()
                                continue
                        else:
                            checkp = 1
                    if checkp == 1:
                        return redirect('/locked/'+title)
                else:
                    return redirect('/locked/'+title)
            i.views += 1
            i.save()
            break
    try:
        print(obj.title)
        try:
            a = notifications.objects.all()
            for i in a:
                if obj in i.relpost.all() and i.status == False:
                    i.status = True
                    i.save()
        except:
            pass
    except:
        return redirect('/')
    if request.user.is_authenticated:
        context = info(request)
    commentdata = {}
    objs = comment.objects.all()
    objs2 = comment_child.objects.all()
    try:
        for i in objs:
            if i.relpost.all()[0] == obj:
                commentdata[i] = {}
                totallength += 1
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
                        totallength += 1
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
    except:
        pass
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
        a['titled'] = i.title
        a['perma'] = i.permalink
        if obj.link_number != i.link_number:
            a['check'] = False
        else:
            a['check'] = True
        if a not in episodes:
            episodes.append(a)
    episodes.sort(key=operator.itemgetter('number'))
    print (episodes)
    context['epilist'] = episodes
    context['postprofileurl'] = profileimg
    context['post'] = obj
    context['postinfor'] = inforobj
    context['cd'] = commentdata.items()
    print (commentdata.items())
    context['totallength'] = totallength
    print (commentdata.items())
    return render(request,template,context)

@login_required(login_url='/loggin')
def comment_new(request,title):
    if request.method == 'POST':
        a = request.POST['comment']
        obj = comment()
        obj.user = request.user
        obj.commentbody = a
        obj.save()
        obj.relpost.add(post.objects.get(permalink = title)) 
        obj.save()
        if request.user != obj.relpost.all()[0].user:
            check = 0
            pobj = pointhistory.objects.filter(user = request.user)
            for i in pobj:
                if i.relpost.all()[0] == obj.relpost.all()[0]:
                    check = 1
                    break
                else:
                    check = 0
            if check == 0:
                pobj = pointhistory()
                pobj.user = request.user
                pobj.note = 'Points earned from comment on the post : '+obj.relpost.all()[0].title+'.'
                pobj.save()
                pobj.relpost.add(obj.relpost.all()[0])
                pobj.save()
                inforobj = infor.objects.get(user=request.user)
                inforobj.points += 3
                inforobj.save()
        obj2 = notifications()
        obj2.user = obj.relpost.all()[0].user
        obj2.sel = 'comment'
        obj2.save()
        obj2.relpost.add(obj.relpost.all()[0])
        obj2.relcom.add(obj)
        obj2.notification = str(obj.user.username)+' ha commentato '+str(title)
        obj2.save()
        a = EmailMessage(
            subject='Commento',
            body=str(title)+' e stato commentato : '+str(html2text(obj.commentbody))+' https://165.227.194.38:8000/post/'+title+ ' https://165.227.194.38:8000/notifications-unread',
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
        obj.save()
        obj.relpost.add(post.objects.get(permalink = title))
        obj.relcomment.add(comment.objects.get(commentbody = body))
        obj.save()
        check = 0
        pobj = pointhistory.objects.filter(user = request.user)
        for i in pobj:
            if i.relpost.all()[0] == obj.relpost.all()[0]:
                check = 1
                break
            else:
                check = 0
        if check == 0:
            pobj = pointhistory()
            pobj.user = request.user
            pobj.note = 'Points earned from comment on the post : '+obj.relpost.all()[0].title+'.'
            pobj.save()
            pobj.relpost.add(obj.relpost.all()[0])
            pobj.save()
            inforobj = infor.objects.get(user=request.user)
            inforobj.points += 3
            inforobj.save()
        return redirect('/post/'+title)

@login_required(login_url='/loggin')
def like_post(request,title):
    obj = post.objects.get(permalink = title)
    objs = obj.likes.all()
    if request.user in objs:
        obj.likes.remove(request.user)
        obj.save()
        return redirect('/post/'+title)
    else:
        obj.likes.add(request.user)
        obj.save()
        obj2 = notifications()
        obj2.user = obj.user
        obj2.notification = request.user.username+' liked your post '+obj.title
        obj2.save()
        obj2.relpost.add(obj)
        obj2.save()
        return redirect('/post/'+title)

@login_required(login_url='/loggin')
def notificationdel(request,id,sel):
    obj = notifications.objects.get(pk=id)
    obj.delete()
    if sel == 1:
        return redirect('/notifications')
    else:
        return redirect('/notifications-unread')

@login_required(login_url='/loggin')
def edit_post(request,title):
    template = 'new-post.html'
    context = info(request)
    obj = post.objects.get(permalink = title)
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
                if i.link_number == 1 and i.linked_post.all().count() < 10:
                    if i.link_title not in a:
                        a.append(i.link_title)
    except:
        pass
    context['series'] = a
    if request.method == 'POST':
        form = contentform(request.POST)
        form2 = titleform(request.POST)
        postdata = request.POST
        a = obj
        a.approved_by_admin = False
        try:
            if form2.is_valid():
                a.title = html2text(form2.cleaned_data['title'])
        except:
            pass
        try:
            if form.is_valid():
                a.content = form.cleaned_data['content']
        except:
            pass
        a.tags = str(postdata['tags'])
        try:
            image = request.FILES['coverimg']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            a.cover = fs.url(filename)
        except:
            pass
        if postdata['action'] == '':
            a.status = 'processing'
        else:
            a.status = 'draft'
        try:
            typ = postdata['post_type']
        except:
            typ = ''
        try:
            seriname = postdata['_new_serie']
        except:
            seriname = ''
        try:
            seri = postdata['post_serie']
        except:
            seri = ''
        if typ == '':
            a.type_of_post = 'single post'
            a.linked_checked = False
            a.link_title = ''
            for i in a.linked_post.all():
                a.linked_post.remove(i)
                i.linked_post.remove(a)
                if i.link_number > a.link_number:
                    i.link_number = i.link_number - 1
                i.save()
            a.link_number = 1
        elif typ == 'new-serie':
            a.type_of_post = 'post part of series'
            a.link_title = seriname
            a.linked_checked = True
            for i in a.linked_post.all():
                a.linked_post.remove(i)
                i.linked_post.remove(a)
                if i.link_number > a.link_number:
                    i.link_number = i.link_number - 1
                i.save()
            a.link_number = 1
            a.linked_post.add(a)
        else:
            a.type_of_post = 'post part of series'
            a.linked_checked = True
            if a.link_title == seri:
                pass
            else:
                for i in a.linked_post.all():
                    a.linked_post.remove(i)
                    i.linked_post.remove(a)
                    if i.link_number > a.link_number:
                        i.link_number = i.link_number - 1
                    i.save()
                for i in post.objects.all():
                    if i.user == request.user and i.link_title == seri:
                        a.linked_post.add(i)
                        i.linked_post.add(a)
                        i.save()
                a.linked_post.add(a)
                a.link_number = a.linked_post.count()
        a.permalink = convertit(a.title)
        a.save()
        return redirect('/edit/'+a.permalink)
    else:
        form = contentform(instance=obj)
        form2 = titleform(instance=obj)
    context['form'] = form
    context['form2'] = form2
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
        try:
            context['main_body'] = request.POST['main-body']
        except:
            context['main_body'] = ''
        context['post'] = request.POST
        print (context)
        context['title'] = html2text(context['post']['title'])
    return render(request,template,context)

def deletepost(request,title):
    obj = post.objects.get(permalink = title)
    obj.delete()
    return redirect('/membri/'+str(request.user.username))

def convertit(a):
    b = ''
    for i in a:
        if i == '\n':
            break
        if i == ' ':
            b = b + '-'
        else:
            b = b + i
    return b

def followunfollow(request,user):
    for i in follow.objects.all():
        if i.user == User.objects.get(username = user) and i.follower == request.user:
            i.delete()
            return redirect('/membri/'+user)
    obj1 = follow()
    obj1.user = User.objects.get(username = user)
    obj1.follower = request.user
    obj1.save()
    obj2 = notifications()
    obj2.user = obj1.user
    obj2.notification = request.user.username + ' ora ti segue'
    obj2.sel = 'follow'
    obj2.save()
    obj2.reluser.add(request.user)
    obj2.save()
    obj3 = userpreferance.objects.get(user = obj1.user)
    if obj3.followed:
        a1 = request.user.username + ' ha cominciato a seguirti \n Per visitare il profilo di '+request.user.username+' clicca qui: https://165.227.194.38:8000/membri/'+request.user.username
        a2 = '\n\n______________\n\nPer disabilitare queste notifiche effettua il login e modifica le impostazioni: https://165.227.194.38:8000/settingsemail'
        email = EmailMessage(
            subject=request.user.username + ' ora ti segue',
            body=a1+a2,
            to = [obj1.user.email]
        )
        email.send()
    return redirect('/membri/'+user)

def followings(request,the_slug):
    context = {'followers':0,'following':0,'posts':0,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
    if request.user.is_authenticated:
        template = 'following.html'
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
            context['followcheck'] = False
            objs = follow.objects.all()
            for i in objs:
                if i.follower == request.user and i.user == context['user2']:
                    context['followcheck'] = True
                    break
            followers = 0
            following = 0
            for i in objs:
                if i.user == context['user2']:
                    followers += 1
                if i.follower == context['user2']:
                    following += 1
            context['followers'] = followers
            context['following'] = following
    else:
        template = 'following-no.html'
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
    objs = follow.objects.all()
    c = {}
    for i in objs:
        if i.follower.username == the_slug:
            obj = infor.objects.get(user=i.user)
            if obj.profile_check == False:
                try:
                    a = obj.user.socialaccount_set.all()[0].provider
                    profileimg = "b"
                except:
                    profileimg = "c"
            else:
                profileimg = "a"
            c[obj] = profileimg
    context['postdata'] = c.items()
    context['posts'] = len(c)
    return render(request,template,context)

def followers(request,the_slug):
    context = {'followers':0,'following':0,'posts':0,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
    if request.user.is_authenticated:
        template = 'followers.html'
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
            context['followcheck'] = False
            objs = follow.objects.all()
            for i in objs:
                if i.follower == request.user and i.user == context['user2']:
                    context['followcheck'] = True
                    break
            followers = 0
            following = 0
            for i in objs:
                if i.user == context['user2']:
                    followers += 1
                if i.follower == context['user2']:
                    following += 1
            context['followers'] = followers
            context['following'] = following
    else:
        template = 'followers-no.html'
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
    objs = follow.objects.all()
    c = {}
    for i in objs:
        if i.user.username == the_slug:
            obj = infor.objects.get(user=i.follower)
            if obj.profile_check == False:
                try:
                    a = obj.user.socialaccount_set.all()[0].provider
                    profileimg = "b"
                except:
                    profileimg = "c"
            else:
                profileimg = "a"
            c[obj] = profileimg
    context['postdata'] = c.items()
    context['posts'] = len(c)
    return render(request,template,context)

@login_required(login_url='/loggin')
def search(request):
    template = 'search.html'
    context = info(request)
    try:
        q = request.GET['s']
    except:
        return redirect('/')
    data1 = []
    for i in post.objects.all():
        if q in i.title and i.approved_by_admin:
            data = {}
            data['posttitle'] = i.title
            data['posturl'] = "post/"+i.permalink
            data['postpic'] = i.cover
            data1.append(data)
    context['postdata'] = data1
    data1 = []
    for i in post.objects.all():
        if q in i.link_title and i.link_number == 1 and i.approved_by_admin:
            data = {}
            data['seriname'] = i.link_title
            data['seriurl'] = "post/"+i.permalink
            data['seripic'] = i.cover
            data1.append(data)
    context['seridata'] = data1
    data1 = []
    for i in infor.objects.all():
        if q in i.user.username:
            data = {}
            data['username'] = i.user.username
            data['userurl'] = "membri/"+i.user.username
            if i.profile_check == False:
                try:
                    profileimg = i.user.socialaccount_set.all()[0].provider
                    profileimg = i.user.socialaccount_set.all()[0].get_avatar_url
                except:
                    profileimg = "/static/profile/"+str(i.profile)+".jpg"
            else:
                profileimg = "/media/"+str(i.profile_pic)
            data['userpic'] = profileimg
            data['user'] = i.user 
            data1.append(data)
    context['userdata'] = data1
    context['lengthofsearch'] = len(context['userdata']) + len(context['postdata']) + len(context['seridata'])
    print(context)
    return render(request,template,context)

def searchapi(request,q):
    data = {'posttitle':'','serititle':'','username':''}
    for i in post.objects.all():
        if q in i.title and i.approved_by_admin:
            data['posttitle'] = i.title
            data['posturl'] = "/post/"+i.permalink
            try:
                data['postpic'] = str(i.cover)
            except:
                data['postpic'] = ''
            break
    for i in post.objects.all():
        if q in i.link_title and i.link_number == 1 and i.approved_by_admin:
            data['seriname'] = i.link_title
            data['seriurl'] = "/post/"+i.permalink
            try:
                data['seripic'] = str(i.cover)
            except:
                data['seripic'] = ''
            break
        print(i.cover)
    for i in infor.objects.all():
        if q in i.user.username:
            data['username'] = i.user.username
            data['userurl'] = "/membri/"+i.user.username
            if i.profile_check == False:
                try:
                    profileimg = i.user.socialaccount_set.all()[0].provider
                    profileimg = i.user.socialaccount_set.all()[0].get_avatar_url
                except:
                    profileimg = "/static/profile/"+str(i.profile)+".jpg"
            else:
                profileimg = "/media/"+str(i.profile_pic)
            data['userpic'] = profileimg
            break
    return JsonResponse(data)

def points(request):
    template = 'punti.html'
    context = info(request)
    context['pointhist'] = pointhistory.objects.filter(user=request.user)
    return render(request,template,context)

def lockedpost(request,title):
    if request.user.is_authenticated:
        template = 'unlock-with-points.html'
        context = info(request)
    else:
        template = 'unlock-with-points-no.html'
        context = {}
    context['title'] = title
    return render(request,template,context)

@login_required(login_url='/loggin')
def unlockpost(request,title):
    obj = post_by_points()
    obj.user = request.user
    obj.post = post.objects.get(permalink=title)
    obj.timestamp = time.time()
    obj.save()
    obj = infor.objects.get(user=request.user)
    obj.points = obj.points - 150
    obj.save()
    return redirect('/post/'+title)