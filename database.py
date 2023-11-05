import psycopg2

class Database:
    def __init__(self, host="localhost", port=5432, user='postgres', password='postgres'):
        self.connection = psycopg2.connect(host=host, port=port, user=user, password=password)
        print("Connected")

Database()