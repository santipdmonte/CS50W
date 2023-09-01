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
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": self.count_followers(),
            "following": self.count_following(),
        }

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    
    def __str__(self):
        return f"{self.title}"
    
    def count_likes(self):
        return self.liked_by.count()
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "edited_at": self.edited_at.strftime("%b %d %Y, %I:%M %p"),
            "edited": self.edited,
            "likes": self.count_likes(),
        }
    





