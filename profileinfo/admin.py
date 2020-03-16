from django.contrib import admin
from .models import *

admin.site.register(follow)
admin.site.register(post)
admin.site.register(comment)
admin.site.register(comment_child)
admin.site.register(notifications)
admin.site.register(post_by_points)
admin.site.register(pointhistory)
admin.site.register(postgallery)
admin.site.register(postgalleryhome)