'''CSV Reader
'''
from sys import stdin
from json import loads
from pathlib import Path
from argparse import ArgumentParser
from . import version
from .logging import LOGGER, log_enable_debug
from ._viewer import spawn_viewer


BANNER = f"Timeline Viewer {version}"


def parse_args():
    '''Parse script arguments
    '''
    parser = ArgumentParser(description="Timeline Viewer")
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        help="Enable debugging output",
    )
    parser.add_argument(
        '--config',
        '-c',
        type=Path,
        help="Configuration file",
    )
    parser.add_argument(
        '--with-header',
        '-w',
        action='store_true',
        help="Consider first line of input as header",
    )
    return parser.parse_args()


def row_reader(headers=None):
    '''Read rows from stdin
    '''
    if headers:
        yield headers
    for line in stdin:
        yield loads(line)['row']


def app():
    LOGGER.info(BANNER)
    args = parse_args()
    log_enable_debug(args.debug)
    headers = None
    if args.config:
        headers = None  #TODO: impl
    spawn_viewer(row_reader(headers), args.with_header)

if __name__ == '__main__':
    app()
