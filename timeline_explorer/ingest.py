'''Ingest module
'''
from csv import reader
from .db import TEDB
from .logging import LOGGER


BATCH_SIZE = 1000


def ingest(csv_path, database_path, wipe=False):
    '''Ingest a CSV and insert it in a database
    '''
    with TEDB(database_path, wipe) as tedb:
        with csv_path.open(newline='') as csv_fp:
            csvreader = reader(csv_fp, dialect='unix')
            line = 1
            csvheader = next(csvreader)
            expected_len = len(csvheader)
            rows = []
            count = 0
            for row in csvreader:
                line += 1
                if len(row) != expected_len:
                    raise RuntimeError(
                        f"invalid CSV file: row does not match the expected number of columns at line {line}"
                    )
                rows.append(row)
                count += 1
                if count == BATCH_SIZE:
                    tedb.insert(rows)
                    rows = []
                    count = 0
            if rows:
                tedb.insert(rows)
    return line - 1
