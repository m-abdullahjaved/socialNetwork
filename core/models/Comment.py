from datetime import datetime
from django.db import models
from .Post import Post
from .Profile import Profile


class Comment(models.Model):
    PostId = models.ForeignKey(Post, on_delete=models.CASCADE)
    Author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Content = models.CharField(max_length=250)
    createdDate = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.Content

    @staticmethod
    def get_all_comments():
        return Comment.objects.all()

    @staticmethod
    def get_comments_by_Post(pid):
        return Comment.objects.filter(PostId=pid)