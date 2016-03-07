from django.db import models
from django.contrib.auth.models import User
from .constants import cartoon_chars, message_types

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    age = models.IntegerField(null=True)
    hobby = models.TextField(null=True)
    character = models.IntegerField(choices=cartoon_chars, null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):  
        return "%s's profile" % self.user  

class Messages(models.Model):
    user = models.ForeignKey(User)
    type =  models.IntegerField(choices=message_types)
    session = models.ForeignKey('Sessions')
    content = models.TextField(null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    
class Sessions(models.Model):
    level = models.IntegerField()
    begin = models.DateTimeField(db_index=True, auto_now_add=True)
    end = models.DateTimeField(db_index=True, auto_now_add=True)