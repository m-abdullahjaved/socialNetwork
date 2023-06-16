import uuid
from django.db import models
from datetime import datetime


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/post_img/')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.caption + " | " + self.user

    @staticmethod
    def get_all_Posts():
        return Post.objects.all()

