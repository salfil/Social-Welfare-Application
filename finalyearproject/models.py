from django.db import models

# Create your models here.
import random

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

from ckeditor.fields import RichTextField
from datetime import datetime, date

#model for staff member.
#each staff member will have these fields
class Staff(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255, blank=True)
    bio=models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile")
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)
    location=models.CharField(max_length=255, null=True, blank=True)
    full_name=models.CharField(max_length=255, blank=True)
    

    def __str__(self):
        return str(self.user.first_name)
    
    #returns preferred url pattern once staff member is registered. 
    def get_absolute_url(self):
        return reverse('home')

#model for program types available. Gives ability to add more if necesary
class ProgrammeType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type

#class for actual programme. 
class Programme(models.Model):
    title=models.CharField(max_length=255)
    type=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    link=models.CharField(max_length=255, null=True, blank=True)
    #relationship with User class as each user will post a programme
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('home')
    

# model for each post category
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

#model for each appointment booking. 
class AppointmentBooking(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    description=models.TextField()
    app_date = models.DateField(null=True, blank=True)  # call date
    app_time = models.TimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=12)
    in_person = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    user_accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    rearranged = models.BooleanField(default=False)
    cancelled = models.BooleanField(default = False)
    completed = models.BooleanField(default = False)
    message = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    key = models.IntegerField(blank=True)
    staff=models.CharField(max_length=100)
    location=models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.first_name 

    def get_absolute_url(self):
        return (reverse('home'))

#Model for each post
class Post(models.Model):
    title = models.CharField(max_length=255)
    #one to one relationship with User model as each staff makes a post
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.CharField(max_length=255, default='general')
    post_date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='like_post')

    def __str__(self):
        return self.title + ' ' + str(self.author)

    def get_absolute_url(self):
        return reverse('home')

#model to add comments on a post.
class Comment(models.Model):
    #each comment relates to a post
    post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    #formats the string using 2 placeholders for the title and name. 
    def __str__(self):
        return '%s -%s' % (self.post.title, self.name)



