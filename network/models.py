from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name='followers', null=True, blank=True)

    def __str__(self):
        return f"{self.username}"

    def follows(self, user):
        if user in self.following.all():
            return True
        return False
    
    def follow_unfollow(self, user):
        if user not in self.following.all():
            self.following.add(user)
        else:
            self.following.remove(user)

    def like_dislike(self, post):
        if self not in post.liked_by.all():
            post.likes += 1
            post.liked_by.add(self)
        else:
            post.likes -= 1
            post.liked_by.remove(self)

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=300)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField('User', related_name='liked_post', null=True, blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} made on {self.posted_on}"
