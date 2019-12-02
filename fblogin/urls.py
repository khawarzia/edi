from django.contrib import admin
from django.urls import path
from login import views as viewslogin
from profileinfo import views as viewsprofile
from django.conf.urls import handler500,url,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

handler500 = 'fblogin.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #home page
    
    path('',viewslogin.status,name='home'),
    
    #login urls

    path('loggin',viewslogin.login,name='login'),
    path('logout',viewslogin.logout,name='logout'),
    path('signup',viewslogin.signup,name='signup'),
    path('reset',viewslogin.reset1,name='reset1'),
    path('new/<str:key>',viewslogin.reset2,name='reset2'),
    
    #profile urls

    path('membri/<str:the_slug>',viewsprofile.profile_page,name='profile'),
    path('drafts',viewsprofile.drafts,name='drafts'),
    path('in_sospeso',viewsprofile.insospeso,name='insos'),
    
    path('membri/<str:the_slug>/viewprofile',viewsprofile.viewprofile,name='view'),
    path('editprofile',viewsprofile.editprofile,name='edit'),
    path('editprofilepic',viewsprofile.editprofilepic,name='editpic'),
    path('deleteprofilepic',viewsprofile.deleteprofilepic,name='deleteprofilepic'),
    path('editprofilecover',viewsprofile.editprofilecover,name='editcover'),
    path('deletecoverpic',viewsprofile.deletecoverpic,name='deletecoverpic'),
    path('randomcover',viewsprofile.randomcover,name='randomcover'),

    path('settingsgeneral',viewsprofile.settingsgeneral,name='setgeneral'),
    path('settingsemail',viewsprofile.settingsemail,name='setemail'),
    path('settingscancel',viewsprofile.settingscancel,name='setcancel'),
    path('deleteaccount',viewsprofile.deleteaccount,name='deleteaccount'),

    path('notifications',viewsprofile.notification_read,name='note'),
    path('notifications-unread',viewsprofile.notification_unread,name='note2'),
    path('deletenotification/<int:id>/<int:sel>',viewsprofile.notificationdel,name='delnote'),

    #posts urls

    path('invia-un-racconto',viewsprofile.new_post,name='new-post'),
    path('post/<str:title>',viewsprofile.view_post,name='view-post'),
    path('edit/<str:title>',viewsprofile.edit_post,name='edit-post'),
    path('post-preview',viewsprofile.preview_post,name='preview-post'),
    path('delete/<str:title>',viewsprofile.deletepost,name='delete-post'),

    #commenting and liking

    path('comment/<str:title>',viewsprofile.comment_new,name='new-comment'),
    path('commentchild/<str:title>/<str:body>',viewsprofile.new_child,name='new-child'),
    path('like/<str:title>',viewsprofile.like_post,name='new-like'),

    #follow and unfollow 

    path('followunfollow/<str:user>',viewsprofile.followunfollow,name='folunfol'),

    #allauth urls for facebook login

    path('account/', include('allauth.urls')),
    
    #media when debug = False

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    #for ckeditor media

    path('ckeditor/',include('ckeditor_uploader.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)