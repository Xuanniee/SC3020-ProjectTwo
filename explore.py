import logging
import time
from typing import Any, Callable, Dict

from Database.database import Database


# ==================== Consts ====================

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
        
        try:
            query = f(op)
        except:
            query = ''

        op['Query'] = query

        if qep:
            fname = qep.store(query)
            if fname:
                op['Filename'] = fname
        return query
    
    return _f


def _rand_id() -> str:
    return '_' + str(int(time.time()*10000000))


# ==================== Operator simulation functions ====================

@store_query
def join(op: "JSON"):
    """Handles join operators
    
    * Nested Loop Inner Join 
    * Hash Join"""

    left = op['Plans'][0]
    right = op['Plans'][1]
    cols = ', '.join(op['Output'])
    join_filter = op.get('Join Filter') 
    qright = f'({right.get("Query")})'

    # Join filter may not be explicitly provided.
    # If unprovided, look at right child for join cond, which usually will be index scan on index cond
    if not join_filter:
        
        # hash join
        join_filter = op.get('Hash Cond')

    if not join_filter:

        # index scan / index only scan
        join_filter = right.get('Index Cond')
    
    if not right.get('Alias'):

        # for joined intermediate results w/o an alias, manually set one as sql syntax requires
        _id_right = _rand_id()

        for col in right['Output']:
            _col = f'{_id_right}.' + '.'.join(col.split('.')[1:])
            cols = cols.replace(col,  _col)
            join_filter = join_filter.replace(col, _col)
            
        right['Alias'] = _id_right

    if not left.get('Alias'):

        # for joined intermediate results w/o an alias, manually set one as sql syntax requires
        _id_left = _rand_id()

        for col in left['Output']:
            _col = f'{_id_left}.' + '.'.join(col.split('.')[1:])
            cols = cols.replace(col,  _col)
            join_filter = join_filter.replace(col, _col)
            
        left['Alias'] = _id_left

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
    return query


@store_query
def scan(op: "JSON"):
    """Scan operators
    
    * Seq Scan
    * Index Scan
    * Index Only Scan"""

    cond = op.get('Filter') or op.get('Index cond')
    cols = ', '.join(op.get('Output', ['*']))

    query = f'''
        SELECT {cols} 
        FROM {op["Relation Name"]} 
        AS {op["Alias"]}
    ''' + (f'WHERE {cond}' if cond else '')
    return query


@store_query
def aggregate(op: "JSON"):
    """Aggregate operators, e.g., SUM(), MIN(), AVG ..."""
    
    _id = _rand_id()
    cols = []
    grpby = []

    # replace column prefixes with alias
    for col in op["Output"]:
        _col = ''
        parts = col.split('.')

        for part in parts[:-1]:
            i = len(part)-1
            while i >= 0 and (part[i].isalnum() or part[i]=='_'):
                i -= 1
            _col += part[:i+1] + _id + '.'

        # un-aggregated columns need to be grouped
        if i == -1:
            grpby.append(parts[-1])
        cols.append(_col + parts[-1])

    query = f'''
        SELECT 
            {", ".join(cols)} 
        FROM 
            (
                {op["Plans"][0]["Query"]}
            ) AS {_id}
        {('GROUP BY ' + ', '.join(grpby)) if grpby else ''}
    '''
    return query


@store_query
def sort(op: "JSON"):
    """Sort operator"""

    return op['Plans'][0]['Query'] + f'\nORDER BY\n{", ".join(op["Sort Key"])}'


@store_query
def limit(op: "JSON"):
    """Limit operator"""

    return op['Plans'][0]['Query'] + f'\nLIMIT {op["Actual Rows"] * op["Actual Loops"]}'

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


    def __enter__(self):
        return self


    def resolve(self):
        """Start operator resolve chain"""

        self._resolve_opt(self.__qep)


    def store(self, query: str) -> str:
        """Run a query and save results in temporary csv file"""

        query_out = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
        fname = f'{_rand_id()}.csv'

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
            
        if _type in ['Nested Loop', 'Hash Join']:
            join(op, qep=self if self.__save else None)
        
        elif _type in ['Seq Scan', 'Index Scan', 'Index Only Scan']:
            scan(op, qep=self if self.__save else None)

        elif _type == 'Aggregate' and op['Partial Mode'] != 'Partial':
            aggregate(op, qep=self if self.__save else None)
        
        else:
            # project child operator's states upwards
            if op.get('Plans'):
                child = op['Plans'][0]
                op['Query'] = child['Query']
                op['Alias'] = child.get('Alias')
            
            logger.debug('Project up:', _type)


    def __exit__(self, *args):
        import os

        logger.info('Exiting QEP ...')

        for file in self.__saved:
            os.remove(file)
            logger.info(f'Removed: {file}')