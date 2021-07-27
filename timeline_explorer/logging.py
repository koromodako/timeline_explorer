'''Logging module
'''
from rich.logging import RichHandler
from logging import getLogger


LOGGER = getLogger('timeline-explorer')
LOGGER.setLevel('INFO')
LOGGER.addHandler(RichHandler(level='DEBUG'))


def log_enable_debug(enable=True):
    '''[summary]
    '''
    LOGGER.setLevel('DEBUG' if enable else 'INFO')
