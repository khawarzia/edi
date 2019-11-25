from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from .models import infor,privacy_policy_and_terms_of_service
from django.core.mail import EmailMessage
import random
from django.forms.models import model_to_dict
from profileinfo.views import info
from profileinfo.models import post,comment,comment_child

def status(request):
    context = {}
    if not (request.user.is_authenticated):
        template = 'index.html'
    else:
        template = 'afterlogin.html'
        context = info(request)
    objp = post.objects.all()
    objs = comment.objects.all()
    objs2 = comment_child.objects.all()
    a = {}
    data = {}
    totallength = 0
    for obj in objp:
        if obj.approved_by_admin == False:
            continue
        commentdata = {}
        data[obj] = {}
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
                commentdata[i]['length'] = totallength
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
                        commentdata[i]['children'][j]['length'] = totallength
        inforobj = infor.objects.get(user=obj.user)
        if inforobj.profile_check == False:
            try:
                a = i.user.socialaccount_set.all()[0].provider
                profileimg = "b"
            except:
                profileimg = "c"
        else:
            profileimg = "a"
        data[obj]['pf'] = profileimg
        data[obj]['cominfor'] = inforobj
        data[obj]['comments'] = totallength
        totallength = 0
        a[obj] = commentdata
    context['data'] = zip(a.items(),data.items())
    print(data)
    return render(request,template,context)

def login(request):
    if request.user.is_authenticated:
        return redirect('/membri/'+str(request.user.username))
    template = 'entry.html'
    if request.method == 'POST':
        a = authenticate(username=request.POST['log'],password=request.POST['pwd'])
        if a is not None:
            auth.login(request,a)
            return redirect(('/membri/'+str(a.username)))
    return render(request,template)

def logout(request):
    auth.logout(request)
    return redirect('/')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/membri/'+str(request.user.username))
    template = 'signupentry.html'
    if request.method == 'POST':
        un = request.POST['username']
        pas = request.POST['password']
        pas1 = request.POST['password1']
        if pas1 != pas:
            context = {'check':0,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
            return render(request,template,context)
        objs = User.objects.all()
        for i in objs:
            if i.username == un:
                context = {'check':1,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
                return render(request,template,context)
        paypal = request.POST['paypalAccount']
        choice = request.POST['user_choice']
        a = User.objects.create_user(
            un,
            request.POST['email'],
            pas
        )
        a.first_name = request.POST['first_name']
        a.save()
        i = infor.objects.get(user=a)
        i.passwordkey = randomizer()
        if paypal != '':
            i.paypal_url = paypal
        i.choice = choice
        i.save()    
        return redirect('/loggin')
    context = {'check':2,'pt':privacy_policy_and_terms_of_service.objects.get(pk=1)}
    return render(request,template,context)

def randomizer():
    a = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    c = ''
    for i in range(0,9):
        c = c + a[random.randint(0,len(a)-1)]
    return c

def reset1(request):
    template = 'resetpass1.html'
    context = {'pt':privacy_policy_and_terms_of_service.objects.get(pk = 1)}
    if request.method == 'POST':
        a = request.POST['user_login']
        objs = User.objects.all()
        for i in objs:
            if a == i.username or a == i.email:
                message = EmailMessage(
                    subject='Reset your password for Edizioniopen.it',
                    body='Go to the following link : \n https://67.207.92.234:8000/new/'+(infor.objects.get(user=i).passwordkey),
                    to=[i.email]
                )
                message.send()
                return redirect('/loggin')
    return render(request,template,context)

def reset2(request,key):
    template = 'resetpass2.html'
    context = {'pt':privacy_policy_and_terms_of_service.objects.get(pk = 1)}
    obj = infor.objects.get(passwordkey = key)
    users = User.objects.all()
    for i in users:
        if i == obj.user:
            userobj = i
    if request.method == 'POST':
        a = request.POST['pass1']
        userobj.set_password(a)
        userobj.save()
        auth.login(request,authenticate(username = userobj.username,password = a))
        return redirect('/membri/'+str(userobj.username))
    return render(request,template,context)
