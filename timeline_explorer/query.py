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
def query(database, select=None, distinct=False, where=None, order_by=None, order=None, limit=None, offset=None):
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
        yield from tedb.select(query)
