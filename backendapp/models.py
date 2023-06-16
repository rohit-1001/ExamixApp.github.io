from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class user1(models.Model):
    email = models.EmailField(max_length=70)
    password = models.CharField(max_length=70)
    checkbox = models.CharField(max_length=70)
    
class user_data(models.Model):
    email = models.EmailField(max_length=70)
    password = models.CharField(max_length=70)
    checkbox = models.CharField(max_length=70)
    
    def __str__(self):
        return self.email
    
class student(models.Model):
    name=models.CharField(max_length=100)
    username=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    phone=models.IntegerField()
    year=models.IntegerField()
    
    def __str__(self):
        return self.name
    
class teacher(models.Model):
    name=models.CharField(max_length=100)
    username=models.IntegerField()
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    phone=models.IntegerField()
    
    def __str__(self):
        return self.name
    
class question(models.Model):
    quizid=models.IntegerField()
    quiz_desc=models.CharField(max_length=400)
    question_no=models.IntegerField()
    question=models.CharField(max_length=400)
    option1=models.CharField(max_length=400)
    option2=models.CharField(max_length=400)
    option3=models.CharField(max_length=400)
    option4=models.CharField(max_length=400)
    answer=models.IntegerField()
    
    def __str__(self):
        return str(self.quizid)
    
class result(models.Model):
    username=models.IntegerField()
    quizid=models.IntegerField()
    question_no=models.IntegerField()
    selected=models.IntegerField()
    actual=models.IntegerField()
    result=models.IntegerField()
    
    def __str__(self):
        return str(self.quizid)


class marks(models.Model):
    username = models.IntegerField()
    quizid = models.IntegerField()
    quiz_desc=models.CharField(max_length=400)
    quiz_status=models.CharField(max_length=50)
    marks = models.IntegerField()

    def __str__(self):
        return str(self.username)
    
    
# class MyUser(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         """Create and save a regular user with the given email and password."""
#         if not email:
#             raise ValueError('Email address must be provided')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         """Create and save a superuser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)