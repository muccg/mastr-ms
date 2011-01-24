import logging, logging.handlers
import os

class LoggingLevelEntry():
    def __init__(self, value, name):
        self._value = value
        self._name = name
    
    @property
    def value(self):
        return self._value
    @property
    def name(self):
        return self._name


class LoggingLevels(object):
    
    INFO = LoggingLevelEntry(logging.INFO, 'info')
    DEBUG = LoggingLevelEntry(logging.DEBUG, 'debug')
    WARNING = LoggingLevelEntry(logging.WARNING, 'warning')
    FATAL = LoggingLevelEntry(logging.FATAL, 'fatal')
    CRITICAL = LoggingLevelEntry(logging.CRITICAL, 'critical')

    @staticmethod
    def getByValue(value):
        for o in [LoggingLevels.INFO, 
                  LoggingLevels.DEBUG, 
                  LoggingLevels.WARNING, 
                  LoggingLevels.FATAL, 
                  LoggingLevels.CRITICAL]:
            if o.value == value:
                return o
        return None        
    @staticmethod
    def getByName(name):
        for o in [LoggingLevels.INFO, 
                  LoggingLevels.DEBUG, 
                  LoggingLevels.WARNING, 
                  LoggingLevels.FATAL, 
                  LoggingLevels.CRITICAL]:
            if o.name == name:
                return o
        return None        

DEBUG = False 
loggers = {}
levels = {}


LOG_DIRECTORY = os.path.join('..', 'data')
LOGGING_LEVEL = LoggingLevels.DEBUG if DEBUG else LoggingLevels.WARNING
LOGGING_FORMATTER = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s:%(message)s")

def getLogger(name):
    if name not in loggers:
        #return logging.getLogger(name) #return python root based named logger
        l = init_logger(name=name, logfile = "%s.log" % (name))
        loggers[name] = l
        return l
    else:
        return loggers[name]

def init_logger(name = "default", logfile = "default.log"):
    #print "logging::init_logger(",name,",",logfile,")"
    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(LOG_DIRECTORY,logfile), 'midnight')
    fh.setFormatter(LOGGING_FORMATTER)
    
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL.value)
    levels[name] = LOGGING_LEVEL
    logger.addHandler(fh)

    return logger

def get_level(name):
    return levels.get(name, None)

def set_level(name, level):
    loggers[name].setLevel(level.value)
    levels[name] = level


'''
def init():
    """Initialise the logger from the settings file..."""
    
    # TODO: improve this
    for logname in settings.LOGS:
        loggers[logname] = init_logger(logname, "%s.log"%logname)
    
init()
'''


#logInitDone=False
#if not logInitDone:
    #logInitDone = True
    #init_logging()
