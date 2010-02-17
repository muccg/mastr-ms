from django.core.mail import send_mail
from madas.settings import RETURN_EMAIL
from webhelpers import siteurl 


def sendFormalQuoteEmail(request, qid, attachmentname, toemail, fromemail=RETURN_EMAIL):
    #The email is sent TO whoever the quote was requested by,
    #and should come FROM the webuser who was logged in and clicked the 'send formal quote' button
    try:
        subject = 'MA Formal Quote'
        body = 'Formal Quote details:\r\n\r\n%s\r\n\r\n' % (attachmentname)
        body += "Please click the following link to view this formal quote on Madas.\r\n\r\n"
        body += "%s%s%s" % (siteurl(request),"quote/viewformal?quoterequestid=" , str(qid))
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail], fail_silently = False)
    except Exception, e:
        print 'Error sending formal quote mail to', toemail, ':', str(e)

def sendFormalStatusEmail(request, qid, status, toemail, fromemail=RETURN_EMAIL):
    #Goes TO an admin or node rep, and comes FROM 
    #TODO: TESTING ONLY: Remove the next line to send to the proper recipients 
    #toemail = 'bpower@ccg.murdoch.edu.au'
     
    try:
        subject = 'MA Formal Quote Status: %s' % (status)
        body = '%s has changed the formal quote status to %s\r\n\r\n' % (fromemail, status) 
        body += "Please click the following link to view this formal quote on Madas.\r\n\r\n"
        body += "%s%s%s" % (siteurl(request),"quote/viewformal?quoterequestid=" , str(qid))
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail], fail_silently = False)
    except Exception, e:
        print 'Error sending formal quote status mail to', toemail, ':', str(e)

def sendQuoteRequestConfirmationEmail(request, qid, toemail, fromemail = RETURN_EMAIL):
    #This email should always come from 'the system' - i.e. the RETURN_EMAIL
    #The confirmation goes 'TO' the user who requested the quote.
    print '\tSending email'
    try:
        subject = 'Madas Quote Request Acknowledgement'
        body = 'Your Madas Quote Request has been added to the system. We will contact you as soon as possible.\r\n\r\n'
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail],fail_silently = False)
    except Exception, e:
        print 'Error sending quote acknowlegement mail to', toemail, ':', str(e)
        
def sendRegistrationToAdminEmail(request, toemail, fromemail=RETURN_EMAIL):
    #This email should always come from 'the system' - i.e. the RETURN_EMAIL
    #The request goes 'TO' an admin or node rep, which is passed in in 'toemail'.
    print '\tSending email'
    try:
        subject = 'New Madas Registration'
        body = 'A new user has registered for Madas. Please follow the link below to review this request.\r\n\r\n'
        body += "Please click the following link to login to Madas.\r\n\r\n"
        body += "%s" % (siteurl(request))
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail],fail_silently = False)
    except Exception, e:
        print 'Error sending mail to Node Reps/Admin: ', toemail , ':', str(e)

def sendQuoteRequestToAdminEmail(request, qid, firstname, lastname, toemail, fromemail=RETURN_EMAIL):
    #This email should always come from 'the system' - i.e. the RETURN_EMAIL
    #The request goes 'TO' an admin or node rep, which is passed in in 'toemail'.
    print '\tSending email'
    try:
        subject = 'Madas Quote Request Requires Attention'
        body = 'A new Madas Quote Request has been added to the system. Please follow the link below to read this request.\r\n\r\n'
        body += "Please click the following link to login to Madas.\r\n\r\n"
        body += "%s" % (siteurl(request))
        body += "\r\n\r\nSender's name or email: %s %s" % (firstname, lastname)
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail],fail_silently = False)
    except Exception, e:
        print 'Error sending mail to Node Reps/Admin: ', toemail , ':', str(e)

def sendAccountModificationEmail(request, toemail, fromemail = RETURN_EMAIL):
    subject = 'Madas Account Change'
    body = 'Your Madas account has been modified\r\n\r\n'
    body += 'Either you, or an administrator has modified your account details or status\r\n\r\n'
    body += 'Please click the following link to login to Madas:\r\n'
    body += '%s\r\n\r\n' % (siteurl(request))
    try:
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail],fail_silently = False)
    except Exception, e:
        print 'Error sending mail to user: ',toemail , ':', str(e)


def sendApprovedRejectedEmail(request, toemail, status, fromemail=RETURN_EMAIL):
    subject = 'Madas Account ' + status
    body = 'Your Madas account was ' + status + '\r\n\r\n'
   

    if status == 'Approved':
        body += 'Please click the following link to login to Madas:\r\n'
        body += '%s\r\n\r\n' % (siteurl(request))
    else:
        body += 'Sorry, no reason was provided\r\n'

    try:
        print '\tSending email from: %s, to: %s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail],fail_silently = False)
    except Exception, e:
        print 'Exception sending mail to user %s: %s' % (toemail , str(e))

def sendForgotPasswordEmail(request, toemail, vk, fromemail = RETURN_EMAIL):
    subject = 'Madas Forgot Password Link'
    body =  "Use the following link to change your Madas password.\r\n\r\n"
    body += "Either you, or someone specifying your email address, has requested a new password for Madas.\r\n\r\n"
    body += "If this was not you, please ignore this email.\r\n\r\n"
    body += "Please click the following link to go to Madas and change your password.\r\n"
    body += "<%slogin/forgotPassword?em=%s&vk=%s>\r\n\r\n" % (siteurl(request), toemail, vk)
    
    try:
        print '\tSending "forgot password" email from:%s to:%s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail], fail_silently = False)
    except Exception, e:
        print '\tException sending mail to %s: %s' % (toemail, str(e))

def sendPasswordChangedEmail(request, toemail, fromemail = RETURN_EMAIL):
    subject = 'Madas Password Changed'
    body = 'Your Madas password was changed.\r\n\r\n'
    body += 'Your password has been changed using the "Forgot Password" feature in Madas.\r\n\r\n'
    body += 'Please click the following link to login to Madas.\r\n\r\n'
    body += siteurl(request) + '\r\n\r\n'
    try:
        print '\tSending "changed password" mail from:%s to:%s' % (fromemail, toemail)
        send_mail(subject, body, fromemail, [toemail], fail_silently = False)
    except Exception, e:
        print '\tException sending mail to %s: %s' % (toemail, str(e))
