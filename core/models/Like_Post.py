from django.db import models


class LikePost(models.Model):
    post_id = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)

    def __str__(self):
        return self.username + " | " + self.post_id
