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
    user = models.ForeignKey(User, null=True)
    type =  models.IntegerField(choices=message_types)
    session = models.ForeignKey('Sessions', null=True)
    content = models.TextField(null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    
class Sessions(models.Model):
    course = models.IntegerField(db_index=True, null=True)
    level = models.IntegerField(null=True)
    step = models.IntegerField(null=True)
    begin = models.DateTimeField(db_index=True, auto_now_add=True)
    end = models.DateTimeField(db_index=True, null=True)
    user = models.ForeignKey(User, null=True)
    correct = models.BooleanField(default=False)
    
class ContentLookUp(models.Model):
    course = models.IntegerField(db_index=True, null=True)
    level = models.IntegerField(db_index=True, null=True)
    step = models.IntegerField(db_index=True, null=True)
    content_pk = models.IntegerField(null=True)
    content_type = models.CharField(max_length=256, null=True)
    answer = models.CharField(max_length=32, null=True)
    
class Training(models.Model):    
    training_accuracy = models.FloatField(default=0, null=True)
    sample_size = models.IntegerField(null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    
class Prediction(models.Model):
    base_personal = models.FloatField(default=0, null=True)
    base_general = models.FloatField(default=0, null=True)
    accumalated = models.FloatField(default=0, null=True)
    current_level = models.IntegerField(null=True)
    correct_num = models.IntegerField(null=True)
    max_currect_momentum = models.IntegerField(null=True)
    aver_speed_at_correct = models.FloatField(default=0, null=True)
    best_speed_at_correct = models.FloatField(default=0, null=True)
    user = models.ForeignKey(User, null=True)
    score = models.FloatField(default=0, null=True)
    next_level = models.IntegerField(null=True)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    
    
    
    
    
    