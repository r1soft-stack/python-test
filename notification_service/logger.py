import logging
from logging import config

# implementation example
# loggerInstance = LoggerService.set_log_level('warning').log({"name": "my name", "levelname": "the message", "message": "message"})


class LoggerService:
    def __init__(self):
        self.level = ""

    @classmethod
    def set_log_level(cls, level='INFO'):
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'format': '[%(asctime)s] %(levelname)s %(message)s',
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

    @classmethod
    def log(cls, message):
        logger = logging.getLogger('notificationService')
        getattr(logger, cls.caller_level)(message)
        return cls

loggerInstance = LoggerService.set_log_level('error').log({"name": "my name", "levelname": "the message", "message": "message"})