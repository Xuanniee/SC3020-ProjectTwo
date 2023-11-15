import psycopg2 as pg
from collections import defaultdict
import csv
import sys
import os

filenames = ['region.csv', 'nation.csv', 'part.csv', 'supplier.csv', 'partsupp.csv', 'customer.csv', 'orders.csv', 'lineitem.csv'];
relations = []

filenameToQuery = {
    'customer.csv': "INSERT INTO public.customer VALUES ", 
    'lineitem.csv': "INSERT INTO public.lineitem VALUES ", 
    'nation.csv': "INSERT INTO public.nation VALUES ", 
    'orders.csv':"INSERT INTO public.orders VALUES ", 
    'part.csv': "INSERT INTO public.part VALUES ", 
    'partsupp.csv': "INSERT INTO public.partsupp VALUES ", 
    'region.csv': "INSERT INTO public.region VALUES ", 
    'supplier.csv': "INSERT INTO public.supplier VALUES "
}

filenameToValuesList = {
    'customer.csv': "(%s, %s, %s, %s, %s, %s, %s, %s)", 
    'lineitem.csv': "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
    'nation.csv': "(%s, %s, %s, %s)", 
    'orders.csv':"(%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
    'part.csv': "(%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
    'partsupp.csv': "(%s, %s, %s, %s, %s)", 
    'region.csv': "(%s, %s, %s)", 
    'supplier.csv': "(%s, %s, %s, %s, %s, %s, %s)"
}

createRegionTable = 'CREATE TABLE IF NOT EXISTS public.region (r_regionkey integer NOT NULL, r_name character(25) COLLATE pg_catalog."default" NOT NULL, r_comment character varying(152) COLLATE pg_catalog."default", CONSTRAINT region_pkey PRIMARY KEY (r_regionkey)) WITH (OIDS = FALSE) TABLESPACE pg_default';
alterRegionTable = 'ALTER TABLE public.region OWNER to postgres';

createNationTable = 'CREATE TABLE IF NOT EXISTS public.nation (n_nationkey integer NOT NULL, n_name character(25) COLLATE pg_catalog."default" NOT NULL, n_regionkey integer NOT NULL, n_comment character varying(152) COLLATE pg_catalog."default", CONSTRAINT nation_pkey PRIMARY KEY (n_nationkey), CONSTRAINT fk_nation FOREIGN KEY (n_regionkey) REFERENCES public.region (r_regionkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
alterNationTable = 'ALTER TABLE public.nation OWNER to postgres';

createPartTable = 'CREATE TABLE IF NOT EXISTS public.part(p_partkey integer NOT NULL, p_name character varying(55) COLLATE pg_catalog."default" NOT NULL, p_mfgr character(25) COLLATE pg_catalog."default" NOT NULL, p_brand character(10) COLLATE pg_catalog."default" NOT NULL, p_type character varying(25) COLLATE pg_catalog."default" NOT NULL, p_size integer NOT NULL, p_container character(10) COLLATE pg_catalog."default" NOT NULL, p_retailprice numeric(15,2) NOT NULL, p_comment character varying(23) COLLATE pg_catalog."default" NOT NULL,CONSTRAINT part_pkey PRIMARY KEY (p_partkey)) WITH (OIDS = FALSE) TABLESPACE pg_default';
alterPartTable = 'ALTER TABLE public.part OWNER to postgres';

createSupplierTable = 'CREATE TABLE IF NOT EXISTS public.supplier (s_suppkey integer NOT NULL, s_name character(25) COLLATE pg_catalog."default" NOT NULL, s_address character varying(40) COLLATE pg_catalog."default" NOT NULL, s_nationkey integer NOT NULL, s_phone character(15) COLLATE pg_catalog."default" NOT NULL, s_acctbal numeric(15,2) NOT NULL, s_comment character varying(101) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT supplier_pkey PRIMARY KEY (s_suppkey), CONSTRAINT fk_supplier FOREIGN KEY (s_nationkey) REFERENCES public.nation (n_nationkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
alterSupplierTable = 'ALTER TABLE public.supplier OWNER to postgres';

createPartsuppTable = 'CREATE TABLE IF NOT EXISTS public.partsupp (ps_partkey integer NOT NULL, ps_suppkey integer NOT NULL, ps_availqty integer NOT NULL, ps_supplycost numeric(15,2) NOT NULL, ps_comment character varying(199) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT partsupp_pkey PRIMARY KEY (ps_partkey, ps_suppkey), CONSTRAINT fk_ps_suppkey_partkey FOREIGN KEY (ps_partkey) REFERENCES public.part (p_partkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT fk_ps_suppkey_suppkey FOREIGN KEY (ps_suppkey) REFERENCES public.supplier (s_suppkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
alterPartsuppTable = 'ALTER TABLE public.partsupp OWNER to postgres';

createCustomerTable = 'CREATE TABLE IF NOT EXISTS public.customer (c_custkey integer NOT NULL, c_name character varying(25) COLLATE pg_catalog."default" NOT NULL, c_address character varying(40) COLLATE pg_catalog."default" NOT NULL, c_nationkey integer NOT NULL, c_phone character(15) COLLATE pg_catalog."default" NOT NULL, c_acctbal numeric(15,2) NOT NULL, c_mktsegment character(10) COLLATE pg_catalog."default" NOT NULL, c_comment character varying(117) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT customer_pkey PRIMARY KEY (c_custkey), CONSTRAINT fk_customer FOREIGN KEY (c_nationkey) REFERENCES public.nation (n_nationkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE)TABLESPACE pg_default';
alterCustomerTable = 'ALTER TABLE public.customer OWNER to postgres';

createOrderTable = 'CREATE TABLE IF NOT EXISTS public.orders (o_orderkey integer NOT NULL, o_custkey integer NOT NULL, o_orderstatus character(1) COLLATE pg_catalog."default" NOT NULL, o_totalprice numeric(15,2) NOT NULL, o_orderdate date NOT NULL, o_orderpriority character (15) COLLATE pg_catalog."default" NOT NULL,  o_clerk character(15) COLLATE pg_catalog."default" NOT NULL, o_shippriority integer NOT NULL, o_comment character varying (79) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT orders_pkey PRIMARY KEY (o_orderkey), CONSTRAINT fk_orders FOREIGN KEY (o_custkey) REFERENCES public.customer (c_custkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE ) TABLESPACE pg_default';
alterOrderTable = 'ALTER TABLE public.orders OWNER to postgres';

createLineitemTable = 'CREATE TABLE IF NOT EXISTS public.lineitem (l_orderkey integer NOT NULL, l_partkey integer NOT NULL, l_suppkey integer NOT NULL, l_linenumber integer NOT NULL, l_quantity numeric(15,2) NOT NULL, l_extendedprice numeric(15,2) NOT NULL, l_discount numeric(15,2) NOT NULL, l_tax numeric(15,2) NOT NULL, l_returnflag character(1) COLLATE pg_catalog."default" NOT NULL, l_linestatus character(1) COLLATE pg_catalog."default" NOT NULL, l_shipdate date NOT NULL, l_commitdate date NOT NULL, l_receiptdate date NOT NULL, l_shipinstruct character(25) COLLATE pg_catalog."default" NOT NULL, l_shipmode character(10) COLLATE pg_catalog."default" NOT NULL, l_comment character varying(44) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT lineitem_pkey PRIMARY KEY (l_orderkey, l_partkey, l_suppkey, l_linenumber), CONSTRAINT fk_lineitem_orderkey FOREIGN KEY (l_orderkey) REFERENCES public.orders (o_orderkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT fk_lineitem_partkey FOREIGN KEY (l_partkey) REFERENCES public.part (p_partkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT fk_lineitem_suppkey FOREIGN KEY (l_suppkey) REFERENCES public.supplier MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
alterLineitemTable = 'ALTER TABLE public.lineitem OWNER to postgres';

# def getPath():
#     cwd = os.getcwd()
#     if os.path.split()

class Database:

    def __init__(self, 
                 DB_NAME = 'tpch', 
                 DB_USER = 'postgres',
                 DB_PASSWORD = 'postgres',
                 DB_HOST = 'localhost',
                 PORT = 5432):
        
        self.DB_NAME = DB_NAME
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DB_HOST = DB_HOST
        self.PORT = PORT

        print('Connecting to client')

        try:
            self.connection = pg.connect(host = DB_HOST,
                       port = PORT,
                       database = DB_NAME,
                       user = DB_USER,
                       password = DB_PASSWORD)
            
            self.cursor = self.connection.cursor()
            print("Connected")
        except:
            print(f'{DB_NAME} does not exist')
            if DB_NAME != 'tpch':
                print(f'Unknown database, please create database {DB_NAME} and insert all data before trying again')
                sys.exit()
            else:
                self.initDB()

        # To get the names of the tables, for generality sake
        self.cursor.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\' AND table_type=\'BASE TABLE\'')
        for tup in self.cursor:
            relations.append(tup[0])

    def closeConnection(self):
        self.cursor.close()
        self.connection.close()

    def initDB(self):
        print("Initialising")

        connection = pg.connect(host = self.DB_HOST,
                       port = self.PORT,
                       database = 'postgres',
                       user = self.DB_USER,
                       password = self.DB_PASSWORD)
        cursor = connection.cursor()

        # Needed to create DB
        connection.autocommit = True

        try:
            cursor.execute(f'CREATE DATABASE {self.DB_NAME}')
            connection.commit()
        except Exception as e:
            print("EXCEPTION", e)
            print("Database TPCH already exists")
        
        cursor.close()
        connection.close()

        connection = pg.connect(host = self.DB_HOST,
                       port = self.PORT,
                       database = self.DB_NAME,
                       user = self.DB_USER,
                       password = self.DB_PASSWORD)
        cursor = connection.cursor()

        self.createTables(connection, cursor)
        self.insertData(connection, cursor)

        self.cursor = cursor
        self.connection = connection

    def createTables(self, connection, cursor):
        print("Creating tables")

        try:
            cursor.execute(createRegionTable)
            cursor.execute(alterRegionTable)

            cursor.execute(createNationTable)
            cursor.execute(alterNationTable)

            cursor.execute(createPartTable)
            cursor.execute(alterPartTable)

            cursor.execute(createSupplierTable)
            cursor.execute(alterSupplierTable)
            
            cursor.execute(createPartsuppTable)
            cursor.execute(alterPartsuppTable)

            cursor.execute(createCustomerTable)
            cursor.execute(alterCustomerTable)

            cursor.execute(createOrderTable)
            cursor.execute(alterOrderTable)

            cursor.execute(createLineitemTable)
            cursor.execute(alterLineitemTable)

            connection.commit()
            
            print("Tables created")
        except Exception as e:
            print(e)
            connection.rollback()
    
    def insertData(self, connection, cursor):
        print("Inserting data")

        for filename in filenames:
            count = 0
            mogrifiedRows = []
            with open(os.path.join(os.path.dirname(__file__), f'../Data/{filename}')) as file:
                reader_obj = csv.reader(file, delimiter='|')

                for row in reader_obj:
                    mogrifiedRows.append(cursor.mogrify(filenameToValuesList[filename], row).decode('utf-8'))
                    if count == 10000:
                        try:
                            args_str = ','.join(mogrifiedRows)
                            cursor.execute(filenameToQuery[filename] + args_str)
                            connection.commit()
                            mogrifiedRows = []
                            count = 0
                            print("Inserted batch into " + filename)
                        except Exception as e:
                            connection.rollback()
                            print(e)
                    count += 1

                if len(mogrifiedRows) != 0:
                    try:
                        args_str = ','.join(mogrifiedRows)
                        cursor.execute(filenameToQuery[filename] + args_str)
                        connection.commit()
                        mogrifiedRows = []
                        count = 0
                        print("Inserted batch into " + filename)
                    except Exception as e:
                        connection.rollback()
                        print(e)
        print("Data inserted")

    def explainQuery(self, query):
        """
        Executes a given query and returns the QEP.

        Parameters:
            query (str): The query to be executed, the method assumes it is a SELECT query.=
        
        returns the QEP for the given query
        """

        self.cursor.execute(f"EXPLAIN (ANALYZE true, COSTS true, VERBOSE true, BUFFERS true, TIMING true, FORMAT JSON) {query}")
        try:
            return self.cursor.fetchall()
        except:
            return []
    
    def query(self, query):
        """
        Executes a given query and returns an array of results.

        Parameters:
            query (str): The query to be executed, the method assumes it is a SELECT query.
        
        ctid is appended after the SELECT keyword in the query so the first item of each row will be the tuple ctid
        """

        temp = query.split(' ')
        query = temp[0] + ' ctid, ' + ' '.join(temp[1:])

        self.cursor.execute(query)
        try:
            return self.cursor.fetchall()
        except:
            return []
        
    
    def getAllBlocksByRelation(self, relation):
        """
        For a relation, returns all the blocks that the relation occupies in the DB

        Parameters:
            relation (str): The name of the relation, eg 'nation'

        Returns a set of block numbers
        """
        relation = relation.lower()

        if relation not in relations:
            print('No relation named', relation)
            return

        self.cursor.execute(f'SELECT ctid FROM {relation}')
        blocks = set()

        for res in self.cursor:
            blocks.add(eval(res[0])[0])
        
        return blocks
    
    def getAllTuplesByBlockNumber(self, relation, blockNum):
        """
        Return all the tuples in the given relation that belong to block blockNum

        Parameters:
            relation (str): The name of the relation, eg 'nation'
            blockNum (int): The block number

        Returns an array of tuples
        """

        relation = relation.lower()

        if relation not in relations:
            print('No relation named', relation)
            return
        
        self.cursor.execute(f'SELECT ctid, * FROM {relation} WHERE (ctid::text::point)[0]={blockNum}')

        return self.cursor.fetchall()
    
    def generateTree(self, query):
        """ 
        Executes a given query and returns the QEP in the form of a tree dictionary.

        Parameters:
            query (str): The query to be executed, the method assumes it is a SELECT query.
        
        returns the QEP for the given query as a dictionary
        """

        QEP = self.explainQuery(query)
        QEP = QEP[0][0][0]['Plan']
        tree = defaultdict(list)
        ids = [1]

        def createTree(plans, level, parent):
            for plan in plans:
                plan['NodeID'] = ids[0]
                plan['ParentNodeID'] = parent
                ids[0] += 1
                if 'Plans' in plan:
                    createTree(plan['Plans'], level+1, plan['NodeID'])
                    del plan['Plans']
                tree[level].append(plan)
        
        if 'Plans' in QEP:
            createTree(QEP['Plans'], 1, 0)
            del QEP['Plans']
            
        QEP['NodeID'] = 0
        QEP['ParentNodeID'] = None
        tree[0] = QEP

        return tree
        


if __name__ == '__main__':
    db = Database()
    print(db.generateTree("SELECT * FROM nation WHERE n_name='ALGERIA' ORDER BY n_nationkey"))
    db.closeConnection()