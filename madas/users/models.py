from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.ForeignKey(User)
    commonName = models.CharField(max_length=255, null=True, blank=True)
    givenName = models.CharField(max_length=255, null=True, blank=True)
    sn = models.CharField(max_length=255, null=True, blank=True)
    mail = models.CharField(max_length=255, null=True, blank=True)
    telephoneNumber = models.CharField(max_length=255, null=True, blank=True)
    homePhone = models.CharField(max_length=255, null=True, blank=True)
    physicalDeliveryOfficeName = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    destinationIndicator = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    postalAddress = models.CharField(max_length=255, null=True, blank=True)
    businessCategory = models.CharField(max_length=255, null=True, blank=True)
    registeredAddress = models.CharField(max_length=255, null=True, blank=True)
    carLicense = models.CharField(max_length=255, null=True, blank=True)

    @property
    def uid(self):
        return self.user.username

    def to_dict(self):
        d = {
            'uid': [self.uid],
            'givenName': [self.givenName],
            'sn': [self.sn],
            'mail': [self.mail],
            'telephoneNumber': [self.telephoneNumber],
            'homePhone': [self.homePhone],
            'physicalDeliveryOfficeName': [self.physicalDeliveryOfficeName],
            'title': [self.title],
            'destinationIndicator': [self.destinationIndicator],
            'description': [self.description],
            'postalAddress': [self.postalAddress],
            'businessCategory': [self.businessCategory],
            'registeredAddress': [self.registeredAddress],
            'carLicense': [self.carLicense]
        }
        return d

class Group(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=255)

