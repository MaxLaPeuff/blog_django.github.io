from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone

class CreateBlog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    intro=models.TextField(default='')
    body = models.TextField()
    image=models.ImageField(upload_to='media', default='' )
    date_created = models.DateTimeField(default=timezone.now)

    class Meta :
        ordering=['-date_created']

class Comment(models.Model):
    post= ForeignKey(CreateBlog,related_name='comments',on_delete=models.CASCADE)
    email=models.EmailField(default='')
    body=models.TextField(default='')
    name=models.CharField(max_length=100,default="inconnu")
    date_added=models.DateTimeField(auto_now=True)

    class Meta :
        ordering=['-date_added']
        