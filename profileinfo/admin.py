from django.contrib import admin
from .models import follow,post,message,comment,comment_child

admin.site.register(follow)
admin.site.register(post)
admin.site.register(message)
admin.site.register(comment)
admin.site.register(comment_child)