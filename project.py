from Database.database import Database
from explore import QEP, generateTree
import json

def main():

    # Generate the database instance and connection, modify the parameters as appropriate
    DB = Database(DB_NAME='tpch', 
                  DB_USER='postgres', 
                  DB_PASSWORD='postgres', 
                  DB_HOST='localhost', 
                  PORT=5432)
    
    query = "SELECT * FROM ( SELECT * FROM nation, region WHERE nation.n_regionkey = region.r_regionkey ORDER BY nation.n_nationkey) AS T1, supplier WHERE T1.n_nationkey = supplier.s_nationkey"

    rawQEP = DB.explainQuery(query)
    rawQEP = rawQEP[0][0][0]

    # Resolves the intermediate results of the QEP
    QEPExecutor =  QEP(rawQEP['Plan'], save=True)
    QEPExecutor.resolve()

    formattedQEPTree = generateTree(qep=rawQEP)
    
    with open('testTree.json', 'w') as out:
        out.write(json.dumps(formattedQEPTree, indent=4))
    
    QEPExecutor.cleanup()


if __name__ == '__main__':
    main()