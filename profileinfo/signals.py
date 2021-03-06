from django.db.models.signals import post_save
from profileinfo.models import post,notifications,follow,comment
from login.models import infor,userpreferance
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from fblogin.settings import EMAIL_HOST_USER,ALLOWED_HOSTS

@receiver(post_save,sender=post)
def email_send(sender,instance,**kwargs):
    if instance.approved_by_admin_check_dont_change == False and instance.approved_by_admin == True:
        instance.approved_by_admin_check_dont_change = True
        instance.save()
        email_add = instance.user.email
        a = EmailMessage(
            subject='LibriCK Approved by Admin',
            body='Your LibriCK with title : '+str(instance.title)+' has been approved by the admin.\nView your post now : https://165.227.194.38:8000/post/'+str(instance.permalink),
            to = [email_add]
        )
        a.send()
        objs = follow.objects.filter(user=instance.user)
        for i in objs:
            if userpreferance.objects.get(user=i.follower).new_librick:
                subject = instance.user.username + ' ha appena pubblicato un LibriCK'
                body = render_to_string('email-message.html',{'post':instance,'host':ALLOWED_HOSTS[0]})
                to = i.follower.email
                send_mail(
                    subject=subject,
                    html_message=body,
                    message=strip_tags(body),
                    from_email=EMAIL_HOST_USER,
                    recipient_list = [to]
                )
            obj = notifications()
            obj.user = i.follower
            obj.sel = 'post'
            obj.notification = instance.user.username+' ha pubblicato '+instance.title
            obj.save()
            obj.relpost.add(instance)
            obj.reluser.add(instance.user)
            obj.save()
        a = 'Your LibriCK with title : '+str(instance.title)+' has been approved by the admin.\nView your post now : https://165.227.194.38:8000/post/'+str(instance.permalink)
        objs = notifications.objects.all()
        for i in objs:
            if i.notification == a:
                return
        obj = notifications()
        obj.user = instance.user
        obj.notification = a
        obj.save()
        obj.relpost.add(instance)
        obj.reluser.add(instance.user)
        obj.save()
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
            if i.user == instance.user and i.notification == 'Congratulazioni, la copertina del tuo Libro è stata aggiunta ai tuo LibriCK!':
                return
        a = notifications()
        a.user = instance.user
        a.notification = 'Congratulazioni, la copertina del tuo Libro è stata aggiunta ai tuo LibriCK!'
        a.save()
        em = EmailMessage(
            subject='Amazon code added',
            body='Congratulazioni, la copertina del tuo Libro è stata aggiunta ai tuo LibriCK!',
            to=[a.user.email]
        )
        em.send()
        try:
            a.relpost.add(linked)
            a.reluser.add(linked.user)
            a.save()
        except:
            pass
    return
