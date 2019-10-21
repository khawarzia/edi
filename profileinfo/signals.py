from django.db.models.signals import post_save
from profileinfo.models import post
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

@receiver(post_save,sender=post)
def email_send(sender,instance,**kwargs):
    email_add = instance.user.email
    a = EmailMessage(
        subject='LibriCK Approved by Admin',
        body='Your LibriCK with title : '+str(instance.titledisplay)+' has been approved by the admin.\nView your post now : https://127.0.0.1:8000/post/'+str(instance.titledisplay),
        to = [email_add]
    )
    a.send()
    return