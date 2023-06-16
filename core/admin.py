from django.contrib import admin
from .models.Profile import Profile
from .models.Post import Post
from .models.Comment import Comment
from .models.Like_Post import LikePost
from .models.FollowersCount import FollowersCount

# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(FollowersCount)