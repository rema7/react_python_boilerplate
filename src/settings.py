import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
LOG_LEVEL = 'ERROR'

DB_CONNECTION = 'postgresql+psycopg2://localhost/r7_editor'

try:
    from settings_local import *
except ModuleNotFoundError:
    pass

REDIS_CONNECTION = 'redis://localhost:6379/0'

DB_CONNECTION_YOYO = DB_CONNECTION.replace('+psycopg2', '')

OFFSET = 100

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['debug_file'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'stream': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'debug_file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'error.log'),
        },
        'access_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'access.log'),
        }
    },
    'loggers': {
        'worker': {
            'level': LOG_LEVEL,
            'handlers': ['stream'],
        },
        'rblb': {
            'level': LOG_LEVEL,
            'handlers': ['error_file', 'debug_file'],
            'propagate': False,
        },
        'gunicorn.error': {
            'level': 'INFO',
            'handlers': ['error_file'],
            'propagate': True,
        },
        'gunicorn.access': {
            'level': 'INFO',
            'handlers': ['access_file'],
            'propagate': False,
        },
    },
}
