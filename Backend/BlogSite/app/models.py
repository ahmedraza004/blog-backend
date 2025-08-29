from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES ={
        "admin": "Admin",
        "author": "Author",
        "reader": "Reader",

    }
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="reader")
    
    bio = models.CharField(max_length=300, null=True, blank=True)


    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.name

    
class Post(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField(null=True,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="catagory")
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)  # 👈 Add this line
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)


    
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True,related_name='post')
    content = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[0:50]
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"