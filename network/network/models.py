from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('User', related_name='followers_of', blank=True)
    following = models.ManyToManyField('User', related_name='following_by', blank=True)

    def __str__(self):
        return f"{self.username}"
    
    def count_followers(self):
        return self.followers.count()
    
    def count_following(self):
        return self.following.count()

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, through='Like')
    
    def __str__(self):
        return f"{self.title}"
    
    def count_likes(self):
        return self.likes.count()
    

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)





