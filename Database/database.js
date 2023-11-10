import pg from 'pg';
import fs from 'fs';
import readline from 'readline';
import format from 'pg-format';
const { Client } = pg;

let DBclient;

const DB_NAME = 'tpch';
const DB_USER = 'postgres';
const DB_PASSWORD = 'postgres';
const DB_HOST = 'localhost';
const PORT = 5432;

const filenames = ['region.csv', 'nation.csv', 'part.csv', 'supplier.csv', 'partsupp.csv', 'customer.csv', 'orders.csv', 'lineitem.csv'];

const filenameToQuery = {
    'customer.csv': "INSERT INTO public.customer VALUES %L", 
    'lineitem.csv': "INSERT INTO public.lineitem VALUES %L", 
    'nation.csv': "INSERT INTO public.nation VALUES %L", 
    'orders.csv':"INSERT INTO public.orders VALUES %L", 
    'part.csv': "INSERT INTO public.part VALUES %L", 
    'partsupp.csv': "INSERT INTO public.partsupp VALUES %L", 
    'region.csv': "INSERT INTO public.region VALUES %L", 
    'supplier.csv': "INSERT INTO public.supplier VALUES %L"
}

const createRegionTable = 'CREATE TABLE IF NOT EXISTS public.region (r_regionkey integer NOT NULL, r_name character(25) COLLATE pg_catalog."default" NOT NULL, r_comment character varying(152) COLLATE pg_catalog."default", CONSTRAINT region_pkey PRIMARY KEY (r_regionkey)) WITH (OIDS = FALSE) TABLESPACE pg_default';
const alterRegionTable = 'ALTER TABLE public.region OWNER to postgres';

const createNationTable = 'CREATE TABLE IF NOT EXISTS public.nation (n_nationkey integer NOT NULL, n_name character(25) COLLATE pg_catalog."default" NOT NULL, n_regionkey integer NOT NULL, n_comment character varying(152) COLLATE pg_catalog."default", CONSTRAINT nation_pkey PRIMARY KEY (n_nationkey), CONSTRAINT fk_nation FOREIGN KEY (n_regionkey) REFERENCES public.region (r_regionkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
const alterNationTable = 'ALTER TABLE public.nation OWNER to postgres';

const createPartTable = 'CREATE TABLE IF NOT EXISTS public.part(p_partkey integer NOT NULL, p_name character varying(55) COLLATE pg_catalog."default" NOT NULL, p_mfgr character(25) COLLATE pg_catalog."default" NOT NULL, p_brand character(10) COLLATE pg_catalog."default" NOT NULL, p_type character varying(25) COLLATE pg_catalog."default" NOT NULL, p_size integer NOT NULL, p_container character(10) COLLATE pg_catalog."default" NOT NULL, p_retailprice numeric(15,2) NOT NULL, p_comment character varying(23) COLLATE pg_catalog."default" NOT NULL,CONSTRAINT part_pkey PRIMARY KEY (p_partkey)) WITH (OIDS = FALSE) TABLESPACE pg_default';
const alterPartTable = 'ALTER TABLE public.part OWNER to postgres';

const createSupplierTable = 'CREATE TABLE IF NOT EXISTS public.supplier (s_suppkey integer NOT NULL, s_name character(25) COLLATE pg_catalog."default" NOT NULL, s_address character varying(40) COLLATE pg_catalog."default" NOT NULL, s_nationkey integer NOT NULL, s_phone character(15) COLLATE pg_catalog."default" NOT NULL, s_acctbal numeric(15,2) NOT NULL, s_comment character varying(101) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT supplier_pkey PRIMARY KEY (s_suppkey), CONSTRAINT fk_supplier FOREIGN KEY (s_nationkey) REFERENCES public.nation (n_nationkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
const alterSupplierTable = 'ALTER TABLE public.supplier OWNER to postgres';

const createPartsuppTable = 'CREATE TABLE IF NOT EXISTS public.partsupp (ps_partkey integer NOT NULL, ps_suppkey integer NOT NULL, ps_availqty integer NOT NULL, ps_supplycost numeric(15,2) NOT NULL, ps_comment character varying(199) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT partsupp_pkey PRIMARY KEY (ps_partkey, ps_suppkey), CONSTRAINT fk_ps_suppkey_partkey FOREIGN KEY (ps_partkey) REFERENCES public.part (p_partkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT fk_ps_suppkey_suppkey FOREIGN KEY (ps_suppkey) REFERENCES public.supplier (s_suppkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
const alterPartsuppTable = 'ALTER TABLE public.partsupp OWNER to postgres';

const createCustomerTable = 'CREATE TABLE IF NOT EXISTS public.customer (c_custkey integer NOT NULL, c_name character varying(25) COLLATE pg_catalog."default" NOT NULL, c_address character varying(40) COLLATE pg_catalog."default" NOT NULL, c_nationkey integer NOT NULL, c_phone character(15) COLLATE pg_catalog."default" NOT NULL, c_acctbal numeric(15,2) NOT NULL, c_mktsegment character(10) COLLATE pg_catalog."default" NOT NULL, c_comment character varying(117) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT customer_pkey PRIMARY KEY (c_custkey), CONSTRAINT fk_customer FOREIGN KEY (c_nationkey) REFERENCES public.nation (n_nationkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE)TABLESPACE pg_default';
const alterCustomerTable = 'ALTER TABLE public.customer OWNER to postgres';

const createOrderTable = 'CREATE TABLE IF NOT EXISTS public.orders (o_orderkey integer NOT NULL, o_custkey integer NOT NULL, o_orderstatus character(1) COLLATE pg_catalog."default" NOT NULL, o_totalprice numeric(15,2) NOT NULL, o_orderdate date NOT NULL, o_orderpriority character (15) COLLATE pg_catalog."default" NOT NULL,  o_clerk character(15) COLLATE pg_catalog."default" NOT NULL, o_shippriority integer NOT NULL, o_comment character varying (79) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT orders_pkey PRIMARY KEY (o_orderkey), CONSTRAINT fk_orders FOREIGN KEY (o_custkey) REFERENCES public.customer (c_custkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE ) TABLESPACE pg_default';
const alterOrderTable = 'ALTER TABLE public.orders OWNER to postgres';

const createLineitemTable = 'CREATE TABLE IF NOT EXISTS public.lineitem (l_orderkey integer NOT NULL, l_partkey integer NOT NULL, l_suppkey integer NOT NULL, l_linenumber integer NOT NULL, l_quantity numeric(15,2) NOT NULL, l_extendedprice numeric(15,2) NOT NULL, l_discount numeric(15,2) NOT NULL, l_tax numeric(15,2) NOT NULL, l_returnflag character(1) COLLATE pg_catalog."default" NOT NULL, l_linestatus character(1) COLLATE pg_catalog."default" NOT NULL, l_shipdate date NOT NULL, l_commitdate date NOT NULL, l_receiptdate date NOT NULL, l_shipinstruct character(25) COLLATE pg_catalog."default" NOT NULL, l_shipmode character(10) COLLATE pg_catalog."default" NOT NULL, l_comment character varying(44) COLLATE pg_catalog."default" NOT NULL, CONSTRAINT lineitem_pkey PRIMARY KEY (l_orderkey, l_partkey, l_suppkey, l_linenumber), CONSTRAINT fk_lineitem_orderkey FOREIGN KEY (l_orderkey) REFERENCES public.orders (o_orderkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT fk_lineitem_partkey FOREIGN KEY (l_partkey) REFERENCES public.part (p_partkey) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION, CONSTRAINT fk_lineitem_suppkey FOREIGN KEY (l_suppkey) REFERENCES public.supplier MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION) WITH (OIDS = FALSE) TABLESPACE pg_default';
const alterLineitemTable = 'ALTER TABLE public.lineitem OWNER to postgres';

export async function setDBClient() {
    console.log('Setting client');
    let client;
    try {
        client = new Client({
            host: DB_HOST,
            port: PORT,
            database: DB_NAME,
            user: DB_USER,
            password: DB_PASSWORD
        });

        await client.connect()
    } catch (e) {
        console.log('TPCH does not exist');
        client = await initDB();
    }

    DBclient = client;
}

export async function closeDBClient() {
    console.log('Closing connection');
    DBclient.end();
}

async function initDB() {
    console.log('Initialising');

    let client = new Client({
        host: DB_HOST,
        port: PORT,
        database: 'postgres',
        user: DB_USER,
        password: DB_PASSWORD
    })

    await client.connect();

    try {
        await client.query(`CREATE DATABASE ${DB_NAME}`);
    } catch (e) {
        console.log("Database TPCH already exists");
    }

    await client.end();

    client = new Client({
        host: DB_HOST,
        port: PORT,
        database: DB_NAME,
        user: DB_USER,
        password: DB_PASSWORD
    });

    await client.connect();
    await createTables(client);
    await insertData(client);

    return client;
}

async function createTables(client) {
    console.log('Creating tables');
    try {
        await client.query('BEGIN');

        await client.query(createRegionTable);
        await client.query(alterRegionTable);

        await client.query(createNationTable);
        await client.query(alterNationTable);

        await client.query(createPartTable);
        await client.query(alterPartTable);

        await client.query(createSupplierTable);
        await client.query(alterSupplierTable);

        await client.query(createPartsuppTable);
        await client.query(alterPartsuppTable);

        await client.query(createCustomerTable);
        await client.query(alterCustomerTable);

        await client.query(createOrderTable);
        await client.query(alterOrderTable);

        await client.query(createLineitemTable);
        await client.query(alterLineitemTable);

        await client.query('COMMIT');
        
        console.log('Tables created');
    } catch (e) {
        console.error(e);
        await client.query('ROLLBACK');
    }
};

async function insertData(client) {
    console.log('Inserting data');
    let dataStream;
    let rl;
    let splitRows;
    let count;
    let rows;
    for (const filename of filenames) {
        count = 0;
        rows = [];
        dataStream = fs.createReadStream(`../Data/${filename}`);
        rl = readline.createInterface({
            input: dataStream,
            crlfDelay: Infinity
        });

        for await (const line of rl) {
            splitRows = line.split('|');
            rows.push(splitRows);
            if (count === 10000) {
                try {
                    await client.query(format(filenameToQuery[filename], rows), []);
                    rows = [];
                    count = 0;
                    console.log(`Inserted batch into ${filename}`);
                } catch (e) {
                    console.error(e);
                }
            }
            count++;
        }
        if (rows.length !== 0) {
            try {
                await client.query(format(filenameToQuery[filename], rows), []);
                rows = [];
                count = 0;
                console.log(`Inserted batch into ${filename}`);
            } catch (e) {
                console.error(e);
            }
        }
    }
    console.log('Data inserted');
}

export function getDBClient() {
    return DBclient;
}

setDBClient().then(async res => {
    closeDBClient();
});