from django.db import models
from django.contrib.auth.models import User, UserManager

class MadasUser(User):
    """User with extra settings"""
    
    #credentials = blah
    #position = models.CharField( max_length=128, blank=True )
    #company = models.CharField( max_length=128, blank=True )
    #city = models.CharField( max_length=128, blank=True )
    #country = models.CharField( max_length=128, default='Australia')
    
    objects = UserManager()
    
