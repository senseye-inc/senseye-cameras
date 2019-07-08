import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s:%(name)s:%(levelname)s %(message)s'
        },
        'simple': {
            'class': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)s:%(name)s:%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'loggers': {
        'senseye_utils': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
        'senseye_cameras': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        },
    }
})
