from django.db.models.signals import post_save
from profileinfo.models import post,notifications
from login.models import infor
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

@receiver(post_save,sender=post)
def email_send(sender,instance,**kwargs):
    if instance.approved_by_admin:
        #email_add = instance.user.email
        #a = EmailMessage(
        #    subject='LibriCK Approved by Admin',
        #    body='Your LibriCK with title : '+str(instance.titledisplay)+' has been approved by the admin.\nView your post now : https://127.0.0.1:8000/post/'+str(instance.titledisplay),
        #    to = [email_add]
        #)
        #a.send()
        a = 'Your LibriCK with title : '+str(instance.title)+' has been approved by the admin.\nView your post now : https://67.207.92.234:8000/post/'+str(instance.permalink)
        objs = notifications.objects.all()
        for i in objs:
            if i.notification == a:
                return
        obj = notifications()
        obj.user = instance.user
        obj.notification = a
        obj.save()
        obj.relpost.add(instance)
        obj.save()
    else:
        pass
    return

@receiver(post_save, sender=infor)
def amazon_code(sender, instance, **kwargs):
    if instance.amazon_code_feature:
        objs = post.objects.all()
        for i in objs:
            if i.user == instance.user:
                linked = i
                break
        objs = notifications.objects.all()
        for i in objs:
            if i.user == instance.user and a.notification == 'Congratulazioni, la copertina del tuo Libro è stata aggiunta ai tuo LibriCK!':
                return
        a = notifications()
        a.user = instance.user
        a.notification = 'Congratulazioni, la copertina del tuo Libro è stata aggiunta ai tuo LibriCK!'
        a.save()
        try:
            a.relpost.add(linked)
            a.save()
        except:
            pass
        return

