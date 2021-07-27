'''Query module
'''
from .db import TEDB, TEDBColumn, TEDBQuery

def query(database, select=None, distinct=False, where=None, order_by=None, order=None, limit=None, offset=None):
    '''Perform a query on the database
    '''
    with TEDB(database) as tedb:
        if select:
            select = [TEDBColumn(col) for col in select]
            if TEDBColumn.ALL in select and len(select) > 1:
                raise ValueError(
                    "Cannot specify column '*' with other columns"
                )
        if order_by:
            order_by = [TEDBColumn(col) for col in order_by]
            if TEDBColumn.ALL in order_by:
                raise ValueError("order_by cannot contain '*' column")
        if order:
            order = TEDBQuery.SortOrder(order)
        query = TEDBQuery(
            select, distinct, where, order_by, order, limit, offset
        )
        if len(select) == 1 and select[0] == TEDBColumn.ALL:
            yield [col.name for col in TEDB.ORDERED_COLUMNS]
        else:
            yield [col.name for col in select]
        yield from tedb.select(query)
