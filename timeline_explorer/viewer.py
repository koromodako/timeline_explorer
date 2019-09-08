'''CSV Reader
'''
# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
from sys import stdin
from json import loads, dumps
from pathlib import Path
from argparse import ArgumentParser
from timeline_explorer import __version__
from .helper.db import TEDB
from .helper.log import app_log, log_enable_debug
from .helper.viewer import spawn_viewer
# ------------------------------------------------------------------------------
# GLOBALS
# ------------------------------------------------------------------------------
__banner__ = r'''Timeline Viewer {}'''.format(__version__)
# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------
def parse_args():
    '''Parse script arguments
    '''
    p = ArgumentParser(description="Timeline Viewer")
    p.add_argument('--debug', '-d', action='store_true', help="Enable debugging output")
    p.add_argument('--config', '-c', type=Path, help="Configuration file")
    p.add_argument('--with-header', '-w', action='store_true', help="Consider first line of input as header")
    return p.parse_args()

def row_reader(headers=None):
    '''Read rows from stdin
    '''
    if headers:
        yield headers
    for line in stdin:
        yield loads(line)['row']

def app():
    app_log.info(__banner__)
    args = parse_args()
    log_enable_debug(args.debug)
    headers = None
    if args.config:
        headers = None  #TODO: impl
    spawn_viewer(row_reader(headers), args.with_header)

if __name__ == '__main__':
    app()
