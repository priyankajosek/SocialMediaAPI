from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    desc = models.CharField(max_length=220)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
  
    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def all_comments(self):
        response = []
        comments = self.comments.all()
        for comment in comments:
            response.append(comment.content)
        return response
        
    def __str__(self):
        return self.title


class Like(models.Model):

    liked_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE,related_name='likes')
    date_created = models.DateTimeField(auto_now_add=True)
      
    def __str__(self):
        return self.liked_by.username


class Comment(models.Model):

    comment_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=220)
    date_created = models.DateTimeField(auto_now_add=True)
      
    def __str__(self):
        return self.comment_by.username


class Follow(models.Model):
    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='followers')
          
    def __str__(self):
        return self.user.username