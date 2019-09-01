# ------------------------------------------------------------------------------
#  IMPORTS
# ------------------------------------------------------------------------------
from termcolor import colored
from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO
# ------------------------------------------------------------------------------
#  CLASSES
# ------------------------------------------------------------------------------
class ColoredFormatter(Formatter):
    '''[summary]
    '''
    COLORS = {
        'DEBUG': 'green',
        'INFO': 'blue',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'magenta'
    }

    def __init__(self, fmt=None, datefmt=None, style='%'):
        '''[summary]
        '''
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        '''[summary]
        '''
        os = super().format(record)
        return colored(os, ColoredFormatter.COLORS[record.levelname], attrs=[])
# ------------------------------------------------------------------------------
#  GLOBALS
# ------------------------------------------------------------------------------
_fmtr = ColoredFormatter('[%(name)s](%(levelname)s)> %(message)s')
_hdlr = StreamHandler()
_hdlr.setFormatter(_fmtr)
app_log = getLogger('tl_explorer')
app_log.setLevel(INFO)
app_log.addHandler(_hdlr)
# ------------------------------------------------------------------------------
#  FUNCTIONS
# ------------------------------------------------------------------------------
def log_enable_debug(enable=True):
    '''[summary]
    '''
    app_log.setLevel(DEBUG if enable else INFO)
