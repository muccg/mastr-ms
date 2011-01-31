from django.contrib import logging
LOGNAME = 'mdatasync_server_log'
logger = logging.getLogger(LOGNAME)
logger.setLevel(logging.WARNING) #the default
print 'Logging level has been restored to WARNING.'
print 'Logging level is ', logger.getEffectiveLevel();

