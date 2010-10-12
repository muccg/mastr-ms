from django.db import models
from django.contrib.auth.models import User

class Emailmap(models.Model):
    id = models.AutoField(primary_key=True) # This field type is a guess.
    emailaddress = models.CharField(max_length=100)
    class Meta:
        db_table = u'emailmap'
        verbose_name = "email map"
        verbose_name_plural = "email maps"

    def __unicode__(self):
        return self.emailaddress


class Quoterequest(models.Model):
    id = models.AutoField(primary_key=True) # This field type is a guess.
    emailaddressid = models.ForeignKey(Emailmap, db_column='emailaddressid')
    tonode = models.CharField(max_length=100)
    details = models.TextField()
    requesttime = models.DateTimeField(auto_now_add=True) #generate 'now' on INSERT
    unread = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    officephone = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    attachment = models.TextField()
    
    class Meta:
        db_table = u'quoterequest'
        verbose_name = "quote request"
        verbose_name_plural = "quote requests"

    def __unicode__(self):
        return "%s (%s,%s)" % (self.tonode, self.lastname, self.firstname)

class Formalquote(models.Model):
    id = models.AutoField(primary_key=True) # This field type is a guess.
    quoterequestid = models.ForeignKey(Quoterequest, db_column='quoterequestid' ) # This field type is a guess.
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #generate 'now' on INSERT
    fromemail = models.CharField(max_length=100)
    toemail = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='new')
    downloaded = models.BooleanField()
    purchase_order_number = models.CharField(max_length=100)
    class Meta:
        db_table = u'formalquote'
        verbose_name = "formal quote"
        verbose_name_plural = "formal quotes"
    def __unicode__(self):
        return str(self.details)



class Quotehistory(models.Model):
    id = models.AutoField(primary_key=True) # This field type is a guess.
    quoteid = models.ForeignKey(Quoterequest, db_column='quoteid' )
    authoremailid = models.ForeignKey(Emailmap, db_column='authoremailid')
    newnode = models.CharField(max_length=100)
    oldnode = models.CharField(max_length=100)
    comment = models.TextField()
    completed = models.BooleanField()
    oldcompleted = models.BooleanField()
    changetimestamp = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = u'quotehistory'
        verbose_name = "quote history"
        verbose_name_plural = "quote histories"


class Organisation(models.Model):
    name = models.CharField(max_length=100)
    abn = models.CharField(max_length=100)
    user = models.ManyToManyField(User, through="UserOrganisation")
    
class UserOrganisation(models.Model):
    user = models.ForeignKey(User)
    organisation = models.ForeignKey(Organisation)
