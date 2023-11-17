import logging
import time
from typing import Any, Callable, Dict
from collections import defaultdict

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

        query = f(op)
        op['Query'] = query

        if qep:
            fname = qep.store(query, f.__name__)
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
    '''
    if join_filter:
        query += f'{op["Join Type"] if op["Join Type"] not in ["Semi", "Cross", "Self", "Anti"] else ""} JOIN\n'
        query += f'{qright} AS {right["Alias"]}\n'
        query += f'ON {join_filter}\n' if join_filter else ''
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
    grpkeys = []

    # replace column prefixes with alias
    for col in op["Output"]:
        _col = ''
        parts = col.split('.')

        for part in parts[:-1]:
            i = len(part)-1
            while i >= 0 and (part[i].isalnum() or part[i] == '_'):
                i -= 1
            _col += part[:i+1] + _id + '.'

        cols.append(_col + parts[-1])

    for key in op.get('Group Key', []):
        _key = ''
        parts = key.split('.')

        for part in parts[:-1]:
            i = len(part)-1
            while i >= 0 and (part[i].isalnum() or part[i] == '_'):
                i -= 1
            _key += part[:i+1] + _id + '.'

        grpkeys.append(_key + parts[-1])

    query = f'''
        SELECT 
            {", ".join(cols)} 
        FROM 
            (
                {op["Plans"][0]["Query"]}
            ) AS {_id}
        {('GROUP BY ' + ', '.join(grpkeys)) if grpkeys else ''}
    '''
    return query


@store_query
def sort_table(op: "JSON"):
    """Sort operator"""

    # remove sort key table prefixes to avoid clashes with alias
    keys = []
    for key in op["Sort Key"]:
        _key = ''
        parts = key.split('.')

        for part in parts[:-1]:
            i = len(part)-1
            while i >= 0 and (part[i].isalnum() or part[i] == '_'):
                i -= 1
            _key += part[:i+1]
        keys.append(_key + parts[-1])

    return op['Plans'][0]['Query'] + f'\nORDER BY\n{", ".join(keys)}'


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
        save: bool = False,
        query: str = None
    ):
        """Iteratively resolve operators from bottom to top, left to right"""

        self.__qep = qep
        self.__save = save
        self.__saved = []
        self.__db = db
        self.__query = query

    def resolve(self):
        """Start operator resolve chain"""

        if self.__query:
            self.__qep['Query'] = self.__query
            for child in self.__qep.get('Plans', []):
                self._resolve_opt(child)
            if self.__save:
                self.__qep['Filename'] = self.store(
                    self.__query, 'scan' if 'Scan' in self.__qep['Node Type'] else '')
        else:
            self._resolve_opt(self.__qep)

    def store(self, query: str, qtype: str) -> str:
        """Run a query and save results in temporary csv file"""

        if qtype == 'scan':
            temp = query.strip().split(' ')
            query = temp[0] + ' ctid, ' + ' '.join(temp[1:])

        query_out = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
        fname = f'{_rand_id()}.csv'

        with open(fname, 'w') as f:
            try:
                self.__db.cursor.copy_expert(query_out, f)
            except Exception as e:
                print(e)
                return

        logger.info(f'Saved to: {fname}')
        logger.debug(f'{query}\n')
        self.__saved.append(fname)

        return fname

    def _resolve_opt(self, op: "JSON") -> bool:
        """Recursively resolve the intermediate operator query plan"""

        _type = op['Node Type']
        failed = False

        for child_op in op.get('Plans', []):
            if not self._resolve_opt(child_op):
                failed = True
        if failed:
            return False

        logger.info(f'Resolving: {_type}')
        _qep = self if self.__save else None
        if _type in ['Nested Loop', 'Hash Join']:
            join(op, qep=_qep)

        elif _type in ['Seq Scan', 'Index Scan', 'Index Only Scan']:
            scan(op, qep=_qep)

        elif (_type == 'Aggregate' and op['Partial Mode'] != 'Partial') or _type == 'Group':
            aggregate(op, qep=_qep)

        elif _type == 'Sort':
            sort_table(op, qep=_qep)

        elif _type == 'Limit':
            limit(op, qep=_qep)

        else:
            # project child operator's states upwards
            if op.get('Plans'):
                child = op['Plans'][0]
                op['Query'] = child['Query']
                op['Alias'] = child.get('Alias')
                if 'Index Cond' not in op:
                    op['Index Cond'] = child.get('Index Cond', None)

            logger.debug(f'Projecting operator upstream: {_type}')
        return op['Query'] != ''

    def cleanup(self):
        import os

        logger.info('Exiting QEP ...')

        for file in self.__saved:
            try:
                os.remove(file)
                logger.info(f'Removed: {file}')
            except:
                pass
        self.__saved.clear()

        for file in os.listdir():
            if file[0] == '_' and file.endswith('.csv'):
                os.remove(file)
                logger.info(f'Removed: {file}')

# ==================== QEP Tree formatter ====================


def generateTree(query=None, qep=None):
    """ 
    Executes a given query and returns the QEP in the form of a tree dictionary.

    Parameters:
        (OPTIONAL) query (str): The query to be executed, the method assumes it is a SELECT query.
        (OPTIONAL) qep (dict): The QEP to format into a tree

        NOTE: Either query or qep must be provided, if both are provided, the query will be ignored.

    returns the formatted QEP tree for the given query as a dictionary along with additional information about the QEP
    """
    if not query and not qep:
        print('Unable to generate tree, either provide a query or a QEP')

    if not qep:
        QEP = db.explainQuery(query)
        additional = QEP[0][0][0]['Planning']
        QEP = QEP[0][0][0]['Plan']
    else:
        additional = qep['Planning']
        QEP = qep['Plan']

    tree = defaultdict(list)

    ids = [1]
    ranking = {}

    def createTree(plans, level, parent):
        for plan in plans:
            plan['NodeID'] = ids[0]
            plan['ParentNodeID'] = parent
            ids[0] += 1
            if 'Plans' in plan:
                createTree(plan['Plans'], level+1, plan['NodeID'])
                del plan['Plans']
            ranking[(plan['Node Type'], plan['NodeID'])
                    ] = float(plan['Total Cost'])
            tree[level].append(plan)

    if 'Plans' in QEP:
        createTree(QEP['Plans'], 1, 0)
        del QEP['Plans']

    QEP['NodeID'] = 0
    QEP['ParentNodeID'] = None
    tree[0].append(QEP)

    additional['Ranking'] = sorted(ranking.items(), key=lambda x: x[1])

    return {'tree': tree, 'additionalInfo': additional}
