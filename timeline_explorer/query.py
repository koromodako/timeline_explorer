'''Query module
'''
# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
from .helper.db import TEDB, TEDBQuery
from .helper.log import app_log
# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------
def query(database, max_width=None,
          select=None, distinct=False,
          where=None,
          order_by=None, order=None,
          limit=None, offset=None):
    '''Perform a query on the database
    '''
    with TEDB(database) as tedb:
        if select:
            select = [TEDB.Column(col) for col in select]
        if order_by:
            order_by = [TEDB.Column(col) for col in order_by]
        if order:
            order = TEDBQuery.SortOrder(order)
        query = TEDBQuery(select, distinct, where, order_by, order, limit, offset)
        for row in tedb.select(query):
            if max_width:
                row = [elt[:max_width] + (elt[max_width:] and '...') for elt in row]
            print(f"| {' | '.join(row)} |")
