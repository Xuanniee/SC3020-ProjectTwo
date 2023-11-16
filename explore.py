import logging
import time
from typing import Any, Callable, Dict

from Database.database import Database


# ==================== Consts ====================

SKIP_NODES = ['Hash', 'Memoize', 'Gather Merge', 'Materialize']
JSON = Dict[str, Any]


# ==================== Global vars ====================

db = Database()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


# ==================== Utility functions ====================

def store_query(f: Callable) -> Callable:
    """Decorator for operator functions.
    
    Write operator outputs to csv as needed."""

    def _f(
        op: "JSON",
        qep: "QEP" = None,
    ) -> str:
        
        query = f(op)

        if qep:
            fname = qep.store(query)
            if fname:
                op['Filename'] = fname
        return query
    
    return _f


@store_query
def join(op: "JSON"):
    """Handles join operators
    
    * Nested Loop Inner Join 
    * Hash Join"""

    left = op['Plans'][0]
    right = op['Plans'][1]
    cols = ','.join(op['Output'])
    join_filter = op.get('Join Filter') 
    qright = f'({right.get("Query")})'

    # Join filter may not be explicitly provided.
    # If unprovided, look at right child for join cond, which usually will be index scan on index cond
    if not join_filter:
        
        # hash join
        join_filter = op.get('Hash Cond')

    if not join_filter:

        # index scan / index only scan
        qright = right['Alias']
        join_filter = right.get('Index Cond')
    
    if not right['Alias']:

        # for joined intermediate results w/o an alias, manually set one as sql syntax requires
        for col in right['Output']:
            _col = '_.' + '.'.join(col.split('.')[1:])
            cols = cols.replace(col,  _col)
            join_filter = join_filter.replace(col, _col)
            
        right['Alias'] = '_'

    query = f'''
        SELECT
            {cols}
        FROM 
            (
                {left['Query']}
            ) AS {left['Alias']}
        {op['Join Type']} JOIN
            {qright} AS {right['Alias']}
        ON
            {join_filter}
    '''
    op['Query'] = query
    return query


@store_query
def scan(op: "JSON"):
    """Scan operators
    
    * Seq Scan
    * Index Scan
    * Index Only Scan"""

    table = op['Relation Name']
    cond = op.get('Filter') or op.get('Index cond')
    cols = ', '.join(op.get('Output', ['*']))

    query = f'SELECT {cols} FROM {table} ' + (f'WHERE {cond}' if cond else '')

    op['Query'] = query
    return query


# ==================== Query Execution Plan handler ====================

class QEP:
    """Takes in a QEP json, calculates all intermediate results which will be saved to file. 

    A new key "Intermediate Results" will be added to every operators, indicating file name of the temporary data dump"""

    def __init__(
        self,
        qep: "JSON",
        save: bool = False
    ):
        """Iteratively resolve operators from bottom to top, left to right"""

        self.__qep = qep
        self.__save = save
        self.__saved = []
        self.__db = db


    def resolve(self):
        """Start operator resolve chain"""

        self._resolve_opt(self.__qep)


    def store(self, query: str) -> str:
        """Run a query and save results in temporary csv file"""

        query_out = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
        fname = f'{time.time()*10000000}.csv'

        with open(fname, 'w') as f:
            try:
                self.__db.cursor.copy_expert(query_out, f)        
            except Exception as e:
                print(e)
                return
        
        logger.info('Saved to:', fname)
        logger.debug(query, '\n')
        self.__saved.append(fname)

        return fname
            

    def _resolve_opt(self, op: "JSON"):
        """Recursively resolve the intermediate operator query plan"""

        _type = op['Node Type']
        logger.info('Resolving:', _type)

        for child_op in op.get('Plans', []):
            self._resolve_opt(child_op)

        if _type in SKIP_NODES:

            # project child operator's states upwards
            child = op['Plans'][0]
            op['Query'] = child['Query']
            op['Alias'] = child.get('Alias')
            
        elif _type in ['Nested Loop', 'Hash Join']:
            join(op, qep=self if self.__save else None)
        elif _type in ['Seq Scan', 'Index Scan', 'Index Only Scan']:
            scan(op, qep=self if self.__save else None)
        else:
            logger.debug('Unable to resolve:', _type)
