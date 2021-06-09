from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    enrolled_courses = models.ManyToManyField('Course', blank=True)

class Post(models.Model):
    title = models.TextField()
    desc = models.TextField()
    video = models.FileField(upload_to='videos', blank=True)
    def __str__(self) -> str:
        return f"{self.title}"

class Course(models.Model):
    thumbnail = models.ImageField(upload_to='thumbnails')
    desc = models.TextField()
    title = models.TextField(default="")
    category = models.TextField(default="")
    posts = models.ManyToManyField(Post, blank=True)
    id = models.AutoField(primary_key=True)
    enrolled_users = models.ManyToManyField(User, blank=True, default='0')
    def enrolled_count(self):
        return self.enrolled_users.all().count()

    def __str__(self) -> str:
        return f"{self.title}"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    message = models.TextField()
    email = models.EmailField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user}"
    
    def serialize(self):
        context = {
            "username" : self.user.username,
            "comment" : self.comment,
            "time" : self.time
        }
        return context