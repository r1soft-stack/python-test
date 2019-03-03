import logging
from logging import config

# implementation example
# loggerInstance = LoggerService.set_log_level('warning').log({"name": "my name", "levelname": "the message", "message": "message"})


class LoggerService:

    """
    This method accept only one parameter. It's look like a setter.
    Here is the place where is possible to define log configurations.
    This method configures file logging handlers for writing one file for each kind of log (INFO, DEBUG, ERROR)
    """
    @classmethod
    def set_log_level(cls, level='INFO'):
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },
            'handlers': {
                'logfile': {
                    'level': level.upper(),
                    'class': 'logging.FileHandler',
                    'filename': 'logs/' + level.upper() + '.log',
                    'formatter': 'simple'
                },
            },
            'loggers': {
                'notificationService': {
                    'handlers': ['logfile'],
                    'level': level.upper()
                },
            },
        })

        cls.level = level.upper()
        cls.caller_level = level.lower()

        return cls

    """
    This method accepts only parameter and it could be string, dict, or any other type.
    The log method corresponding to caller_level will be called.
    The logger instance given by the getLogger is defined in the set_log_level method
    """
    @classmethod
    def log(cls, message):
        logger = logging.getLogger('notificationService')
        getattr(logger, cls.caller_level)(message)
        return cls