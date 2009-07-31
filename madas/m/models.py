from django.db import models

class Emailmap(models.Model):
    id = models.AutoField(primary_key=True) # This field type is a guess.
    emailaddress = models.CharField(max_length=100)
    class Meta:
        db_table = u'emailmap'


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


class Formalquote(models.Model):
    id = models.AutoField(primary_key=True) # This field type is a guess.
    quoterequestid = models.ForeignKey(Quoterequest, db_column='quoterequestid' ) # This field type is a guess.
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True) #generate 'now' on INSERT
    fromemail = models.CharField(max_length=100)
    toemail = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='new')
    downloaded = models.BooleanField()
    class Meta:
        db_table = u'formalquote'


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


