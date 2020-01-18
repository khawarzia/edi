from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message, UserProfile
from chat.serializers import MessageSerializer, UserSerializer
from login.models import infor

@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = infor.objects.filter(user = User.objects.get(id=pk))
        else:
            users = []
            for i in Message.objects.all():
                if i.sender == request.user or i.receiver == request.user:
                    a = infor.objects.get(user=i.sender)
                    b = infor.objects.get(user=i.receiver)
                    if a not in users:
                        users.append(a)
                    if b not in users:
                        users.append(b)
        data = []
        for i in users:
            a = {'id':i.user.id,'username':i.user.username}
            try:
                a['online'] = UserProfile.objects.get(user=i.user).online()
            except:
                obj = UserProfile()
                obj.user = i.user
                obj.save()
                a['online'] = obj.online()
            if i.profile_check == False:
                try:
                    profileimg = i.user.socialaccount_set.all()[0].provider
                    profileimg = i.user.socialaccount_set.all()[0].get_avatar_url()
                except:
                    profileimg = "/static/profile/"+str(i.profile)+".jpg"
            else:
                profileimg = "/media/"+str(i.profile_pic)
            a['profileurl'] = profileimg
            data.append(a)
        return JsonResponse(data,safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)

@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})