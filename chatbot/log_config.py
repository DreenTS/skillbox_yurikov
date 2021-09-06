import logging.config

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'bot_logger_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%d-%m-%Y %H:%M',
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'bot_logger_formatter',
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'bot_logger_formatter',
            'filename': 'bot.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'bot_logger': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': 'DEBUG',
        },
    },
}


def configure_logger():
    logging.config.dictConfig(LOG_CONFIG)
    log = logging.getLogger('bot_logger')
    return log


if __name__ == '__main__':
    bot_logger = logging.getLogger('bot_logger')
    print('Done!!!')
