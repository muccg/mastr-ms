from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Extended user model.
    This could be renamed to something less confusing.
    """
    commonName = models.CharField(max_length=255, blank=True)
    givenName = models.CharField(max_length=255, blank=True)
    sn = models.CharField(max_length=255, blank=True)
    mail = models.CharField(max_length=255, blank=True)
    telephoneNumber = models.CharField(max_length=255, blank=True)
    homePhone = models.CharField(max_length=255, blank=True)
    physicalDeliveryOfficeName = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    destinationIndicator = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    postalAddress = models.CharField(max_length=255, blank=True)
    businessCategory = models.CharField(max_length=255, blank=True)
    registeredAddress = models.CharField(max_length=255, blank=True)
    carLicense = models.CharField(max_length=255, blank=True)
    passwordResetKey = models.CharField(max_length=255, blank=True)

    @property
    def uid(self):
        return self.username

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
                val = d.get(attr)
                if isinstance(val, list):
                    val = val[0]
                setattr(self, attr, val)
