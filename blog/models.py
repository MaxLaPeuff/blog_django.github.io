from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.contrib.auth.models import User 

class CreateBlog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    intro=models.TextField(default='')
    body = models.TextField()
    image=models.ImageField(upload_to='media', default='')
    date_created = models.DateTimeField(default=timezone.now)

class Meta :
        ordering=['-date_created']

class Comment(models.Model):
    post = models.ForeignKey(CreateBlog, related_name='comments', on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    body = models.TextField(default='')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'Comment by {self.user_comment.username} on {self.post.title}'
