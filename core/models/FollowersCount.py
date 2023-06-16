from django.db import models


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

    @staticmethod
    def count_following(id):
        return len(FollowersCount.objects.filter(follower=id))