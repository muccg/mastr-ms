from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.OneToOneField(User)
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
    passwordResetKey = models.CharField(max_length=255, null=True, blank=True)

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
            'carLicense': [self.carLicense],
            'passwordResetKey': [self.passwordResetKey]
        }
        return d

    def set_from_dict(self, d):
        for attr in ('givenName','sn','mail','telephoneNumber', 'homePhone', 'physicalDeliveryOfficeName', 'title',
                     'destinationIndicator', 'description', 'postalAddress', 'businessCategory', 'registeredAddress',
                     'carLicense', 'passwordResetKey'):
            if d.get(attr):
                setattr(self, attr, d.get(attr))


class Group(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=255, unique=True)

