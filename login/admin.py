from django.contrib import admin
from .models import infor,privacy_policy_and_terms_of_service,userpreferance

admin.site.register(infor)
admin.site.register(privacy_policy_and_terms_of_service)
admin.site.register(userpreferance)