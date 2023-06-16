from django.urls import path
from .Views.Home import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('setting', setting),
    path('upload', upload, name='upload'),
    path('follow', follow, name='follow'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('profile/<str:pk>', profile, name='profile'),
    path('logout', logout, name='logout'),
    path('likepost', likepost, name='likepost'),
    path('add_comment', add_comment, name='add_comment')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)