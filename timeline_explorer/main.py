'''CSV Reader
'''
# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
from json import loads, dumps
from pathlib import Path
from argparse import ArgumentParser
from timeline_explorer import __version__
from .query import query
from .ingest import ingest
from .helper.db import TEDB
from .helper.log import app_log, log_enable_debug
# ------------------------------------------------------------------------------
# GLOBALS
# ------------------------------------------------------------------------------
__banner__ = r'''
 _____ _                _ _              _____            _
|_   _(_)_ __ ___   ___| (_)_ __   ___  | ____|_  ___ __ | | ___  _ __ ___ _ __
  | | | | '_ ` _ \ / _ \ | | '_ \ / _ \ |  _| \ \/ / '_ \| |/ _ \| '__/ _ \ '__|
  | | | | | | | | |  __/ | | | | |  __/ | |___ >  <| |_) | | (_) | | |  __/ |
  |_| |_|_| |_| |_|\___|_|_|_| |_|\___| |_____/_/\_\ .__/|_|\___/|_|  \___|_|
                                                   |_|                        {}
'''.format(__version__)
# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------
def info_cmd(args):
    '''Give some information
    '''
    print("Columns:")
    for col in TEDB.Column:
        print(f"  - {col.value}")

def ingest_cmd(args):
    '''Load a CSV into a SQLite database
    '''
    count = ingest(args.csv, args.database, args.wipe)
    print(f"{count} lines inserted into {args.database}")

def query_cmd(args):
    '''Perform a query on the database
    '''
    if args.config:
        conf = loads(args.config.read_text())
        if isinstance(args.select, str):
            args.select = args.select.split(',')
        args.select = conf.get('select', args.select)
        args.distinct = conf.get('distinct', args.distinct)
        args.where = conf.get('where', args.where)
        if isinstance(args.order_by, str):
            args.order_by = args.order_by.split(',')
        args.order_by = conf.get('order_by', args.order_by)
        args.order = conf.get('order', args.order)
        args.limit = conf.get('limit', args.limit)
        args.offset = conf.get('offset', args.offset)
        args.max_width = conf.get('max_width', args.max_width)
    for row in query(args.database, args.select, args.distinct, args.where, args.order_by, args.order, args.limit, args.offset):
        if args.max_width:
            row = [elt[:args.max_width] + (elt[args.max_width:] and '...') for elt in row]
        print(f"| {' | '.join(row)} |")

def parse_args():
    '''Parse script arguments
    '''
    p = ArgumentParser(description="CSV Reader")
    p.add_argument('--debug', '-d', action='store_true', help="Enable debugging output")
    p.add_argument('--database', type=Path, default=TEDB.DEFAULT_DB, help="Database to be written")
    subparsers = p.add_subparsers(dest='command')
    subparsers.required = True
    # info parser
    info_p = subparsers.add_parser('info')
    info_p.set_defaults(cmd_func=info_cmd)
    # ingest parser
    ingest_p = subparsers.add_parser('ingest')
    ingest_p.set_defaults(cmd_func=ingest_cmd)
    ingest_p.add_argument('--wipe', action='store_true', help="Set to wipe the database if already existing")
    ingest_p.add_argument('csv', type=Path, help="CSV file to be read")
    # query parser
    query_p = subparsers.add_parser('query')
    query_p.set_defaults(cmd_func=query_cmd)
    query_p.add_argument('--config', '-c', type=Path, help="Query configuration file (JSON formatted values for query arguments)")
    query_p.add_argument('--order', default='asc', help="Choose between ascending (asc) and descending (desc)")
    query_p.add_argument('--order-by', help="Comma separated list of columns")
    query_p.add_argument('--select', default='*', help="Comma separated list of columns to display")
    query_p.add_argument('--distinct', action='store_true', help="Display only unique rows")
    query_p.add_argument('--where', help="Condition to select a row")
    query_p.add_argument('--limit', type=int, help="Limit number of results")
    query_p.add_argument('--offset', type=int, help="Start reading results from offset. Only valid if --limit is set")
    query_p.add_argument('--max-width', type=int, help="Max width for each column")
    return p.parse_args()

def app():
    print(__banner__)
    args = parse_args()
    log_enable_debug(args.debug)
    try:
        args.cmd_func(args)
    except BrokenPipeError:
        app_log.warning("Pipe error, failed to write more data to pipe.")
    except:
        app_log.exception("An exception occured.")

if __name__ == '__main__':
    app()
