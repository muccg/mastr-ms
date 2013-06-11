from django.core.mail import send_mail
from django.conf import settings
from ccg.utils.webhelpers import siteurl
from django.core.mail import EmailMessage
import logging
from mastrms.users.MAUser import MADAS_USER_GROUP

logger = logging.getLogger('madas_log')

class FixedEmailMessage(EmailMessage):
    def __init__(self, subject='', body='', from_email=None, to=None, cc=None,
                 bcc=None, connection=None, attachments=None, headers=None):
        """
        Initialize a single email message (which can be sent to multiple
        recipients).

        All strings used to create the message can be Unicode strings (or UTF-8
        bytestrings). The SafeMIMEText class will handle any necessary encoding
        conversions.
        """
        to_cc_bcc_types = (type(None), list, tuple)
        try:
            # test for typical error: people put strings in to, cc and bcc fields
            # see documentation at http://www.djangoproject.com/documentation/email/
            assert isinstance(to, to_cc_bcc_types)
            assert isinstance(cc, to_cc_bcc_types)
            assert isinstance(bcc, to_cc_bcc_types)
            super(FixedEmailMessage, self).__init__(subject, body, from_email, to,
                                           bcc, connection, attachments, headers)
            if cc:
                self.cc = list(cc)
            else:
                self.cc = []

        except AssertionError, e:
            logger.warning('Arguments to FixedEmailMessage were incorrect: %s' % (str(e)) )

    def recipients(self):
        """
        Returns a list of all recipients of the email (includes direct
        addressees as well as Bcc entries).
        """
        return self.to + self.cc + self.bcc

    def message(self):
        msg = super(FixedEmailMessage, self).message()
        del msg['Bcc'] # if you still use old django versions
        if self.cc:
            msg['Cc'] = ', '.join(self.cc)
        return msg

    def sendMail(self):
        try:
            logger.debug('\tSending email (subject=%s) from: %s, to: %s' % (subject, self.fromemail, self.toemail))
            self.send()
        except Exception, e:
            logger.warning('Error sending email (subject=%s) to %s : %s' %(subject, toemail, str(e)) )


def makeAndSendMail(subject, body, from_email, to, fail_silently=False):
    '''Note: the to param should be a list, even for one recipient'''
    try:
        logger.debug('\tSending email (subject=%s) from: %s, to: %s' % (subject, from_email, to))
        send_mail(subject, body, from_email, to, fail_silently = False)
    except Exception, e:
        logger.warning('Error sending email (subject=%s) to %s : %s' %(subject, to, str(e)) )

def sendFormalQuoteEmail(request, qid, attachmentname, toemail, cclist=None, fromemail=settings.RETURN_EMAIL):
    #The email is sent TO whoever the quote was requested by,
    #and should come FROM the webuser who was logged in and clicked the 'send formal quote' button
    subject = 'MA Formal Quote'
    body = 'Formal Quote details:\r\n\r\n%s\r\n\r\n' % (attachmentname)
    body += "Please click the following link to view this formal quote on Madas.\r\n\r\n"
    body += "%s%s%s" % (siteurl(request),"quote/viewformal?quoterequestid=" , str(qid))
    e = FixedEmailMessage(subject=subject, body=body, from_email = fromemail, to = [toemail], cc=cclist)
    e.sendMail()

def sendFormalStatusEmail(request, qid, status, toemail, fromemail=settings.RETURN_EMAIL):
    #Goes TO an admin or node rep, and comes FROM the default return email
    subject = 'MA Formal Quote Status: %s' % (status)
    body = '%s has changed the formal quote status to %s\r\n\r\n' % (fromemail, status)
    body += "Please click the following link to view this formal quote on Madas.\r\n\r\n"
    body += "%s%s%s" % (siteurl(request),"quote/viewformal?quoterequestid=" , str(qid))
    makeAndSendMail(subject, body, fromemail, [toemail], fail_silently = False)

def sendQuoteRequestConfirmationEmail(request, qid, toemail, fromemail = settings.RETURN_EMAIL):
    #This email should always come from 'the system' - i.e. the RETURN_EMAIL
    #The confirmation goes 'TO' the user who requested the quote.
    subject = 'Madas Quote Request Acknowledgement'
    body = 'Your Madas Quote Request has been added to the system. We will contact you as soon as possible.\r\n\r\n'
    makeAndSendMail(subject, body, fromemail, [toemail],fail_silently = False)

def sendRegistrationToAdminEmail(request, username, toemail, fromemail=settings.RETURN_EMAIL):
    #This email should always come from 'the system' - i.e. the RETURN_EMAIL
    #The request goes 'TO' an admin or node rep, which is passed in in 'toemail'.
    subject = 'New Madas Registration'
    body = 'A new user has registered for Madas. Please follow the link below to review this request.\r\n\r\n'
    body += "Their e-mail address is %s.\r\n\r\n" % username
    body += "Please click the following link to login to Madas.\r\n\r\n"
    body += "%s" % (siteurl(request))
    makeAndSendMail(subject, body, fromemail, [toemail],fail_silently = False)

def sendQuoteRequestToAdminEmail(request, qid, firstname, lastname, toemail, fromemail=settings.RETURN_EMAIL):
    #This email should always come from 'the system' - i.e. the RETURN_EMAIL
    #The request goes 'TO' an admin or node rep, which is passed in in 'toemail'.
    subject = 'Madas Quote Request Requires Attention'
    body = 'A new Madas Quote Request has been added to the system. Please follow the link below to read this request.\r\n\r\n'
    body += "Please click the following link to login to Madas.\r\n\r\n"
    body += "%s" % (siteurl(request))
    body += "\r\n\r\nSender's name or email: %s %s" % (firstname, lastname)
    makeAndSendMail(subject, body, fromemail, [toemail],fail_silently = False)

def sendAccountModificationEmail(request, toemail, fromemail = settings.RETURN_EMAIL):
    subject = 'Madas Account Change'
    body = 'Your Madas account has been modified\r\n\r\n'
    body += 'Either you, or an administrator has modified your account details or status\r\n\r\n'
    body += 'Please click the following link to login to Madas:\r\n'
    body += '%s\r\n\r\n' % (siteurl(request))
    makeAndSendMail(subject, body, fromemail, [toemail],fail_silently = False)


def sendApprovedRejectedEmail(request, toemail, status, fromemail=settings.RETURN_EMAIL):
    if status == MADAS_USER_GROUP:
        status = 'Approved'
    subject = 'Madas Account ' + status
    body = 'Your Madas account was ' + status + '\r\n\r\n'


    if status == 'Approved':
        body += 'Please click the following link to login to Madas:\r\n'
        body += '%s\r\n\r\n' % (siteurl(request))
    else:
        body += 'Sorry, no reason was provided\r\n'

    makeAndSendMail(subject, body, fromemail, [toemail],fail_silently = False)

def sendForgotPasswordEmail(request, toemail, vk, fromemail = settings.RETURN_EMAIL):
    subject = 'Madas Forgot Password Link'
    body =  "Use the following link to change your Madas password.\r\n\r\n"
    body += "Either you, or someone specifying your email address, has requested a new password for Madas.\r\n\r\n"
    body += "If this was not you, please ignore this email.\r\n\r\n"
    body += "Please click the following link to go to Madas and change your password.\r\n"
    body += "<%slogin/forgotPassword?em=%s&vk=%s>\r\n\r\n" % (siteurl(request), toemail, vk)

    makeAndSendMail(subject, body, fromemail, [toemail], fail_silently = False)

def sendPasswordChangedEmail(request, toemail, fromemail = settings.RETURN_EMAIL):
    subject = 'Madas Password Changed'
    body = 'Your Madas password was changed.\r\n\r\n'
    body += 'Your password has been changed using the "Forgot Password" feature in Madas.\r\n\r\n'
    body += 'Please click the following link to login to Madas.\r\n\r\n'
    body += siteurl(request) + '\r\n\r\n'
    makeAndSendMail(subject, body, fromemail, [toemail], fail_silently = False)
