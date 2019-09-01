'''[summary]

'''
# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
import sqlite3
from enum import Enum
from pathlib import Path
from .log import app_log
# ------------------------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------------------------
def cjoin(cols):
    return ', '.join(cols)
# ------------------------------------------------------------------------------
# CLASSES
# ------------------------------------------------------------------------------
class TEDBQuery:
    '''Represent a query which can be made on a TEDB
    '''
    class SortOrder(Enum):
        '''Sort order
        '''
        ASC = 'asc'
        DESC = 'desc'

    def __init__(self, select=None, distinct=False,
                 where=None,
                 order_by=None, order=None,
                 limit=None, offset=None):
        '''Constructor
        '''
        self._select = select or ['*']
        self._distinct = distinct
        self._where = where
        self._order_by = order_by
        self._order = order or SelectQuery.SortOrder.ASC
        self._limit = limit
        self._offset = offset

    def statement(self, table_name):
        '''SQL statement representation of the query
        '''
        stmt = [f"SELECT {cjoin([col.value for col in self._select])}"]
        if self._distinct:
            stmt.append("DISTINCT")
        stmt.append(f"FROM {table_name}")
        if self._where:
            stmt.append(f"WHERE {self._where}")
        if self._order_by:
            stmt.append(f"ORDER BY {cjoin([col.value for col in self._order_by])} {self._order.name}")
        if self._limit:
            stmt.append(f"LIMIT {self._limit}")
            if self._offset:
                stmt.append(f"OFFSET {self._offset}")
        return ' '.join(stmt)

class TEDB:
    '''Timeline Explorer Database
    '''
    class Column(Enum):
        '''Timeline Explorer Database columns
        '''
        ALL = '*'
        DATE = 'c_date'
        TIME = 'c_time'
        TIMEZONE = 'c_timezone'
        MACB = 'c_macb'
        SOURCE = 'c_source'
        SOURCETYPE = 'c_sourcetype'
        TYPE = 'c_type'
        USER = 'c_user'
        HOST = 'c_host'
        SHORT = 'c_short'
        DESC = 'c_desc'
        VERSION = 'c_version'
        FILENAME = 'c_filename'
        INODE = 'c_inode'
        NOTES = 'c_notes'
        FORMAT = 'c_format'
        EXTRA = 'c_extra'
    # default values
    DEFAULT_DB = Path('.timeline_explorer.db')
    # the list below defines the order of columns
    ORDERED_COLUMNS = [
        Column.DATE,
        Column.TIME,
        Column.TIMEZONE,
        Column.MACB,
        Column.SOURCE,
        Column.SOURCETYPE,
        Column.TYPE,
        Column.USER,
        Column.HOST,
        Column.SHORT,
        Column.DESC,
        Column.VERSION,
        Column.FILENAME,
        Column.INODE,
        Column.NOTES,
        Column.FORMAT,
        Column.EXTRA,
    ]
    # SQL statements
    TABLE_NAME = 'te_tb'
    INSERT_INTO_STMT = f"INSERT INTO {TABLE_NAME} VALUES ({cjoin(['?' for col in ORDERED_COLUMNS])})"
    CREATE_TABLE_STMT = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME}({cjoin([col.value for col in ORDERED_COLUMNS])})"
    DELETE_STMT = f"DELETE FROM {TABLE_NAME}"

    def __init__(self, path=None, wipe=False):
        '''Constructor
        '''
        self._path = path or self.DEFAULT_DB
        if wipe and path.is_file():
            path.unlink()
            app_log.info(f"{path} wiped.")
        self._conn = None

    def __enter__(self):
        '''Context manager enter
        '''
        self._conn = sqlite3.connect(str(self._path))
        cur = self._conn.cursor()
        cur.execute(self.CREATE_TABLE_STMT)
        self._conn.commit()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        '''Context manager exit
        '''
        self._conn.commit()
        self._conn.close()

    @property
    def path(self):
        '''DB file path
        '''
        return self._path

    def insert(self, rows):
        '''Insert some records in the table
        '''
        cur = self._conn.cursor()
        for row in rows:
            cur.execute(self.INSERT_INTO_STMT, row)
        self._conn.commit()

    def select(self, query):
        '''Select some records in the table based on the query
        '''
        cur = self._conn.cursor()
        cur.execute(query.statement(self.TABLE_NAME))
        while True:
            row = cur.fetchone()
            if not row:
                break
            yield row

    def clear(self):
        '''Clear the table from all its records
        '''
        cur = self._conn.cursor()
        cur.execute(self.DELETE_STMT)
        self._conn.commit()
