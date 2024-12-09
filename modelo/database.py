# modelo/database.py

import psycopg2
from psycopg2 import pool

class Database:
    _connection_pool = None

    @staticmethod
    def initialize(**kwargs):
        Database._connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **kwargs)

    @staticmethod
    def get_connection():
        if Database._connection_pool:
            return Database._connection_pool.getconn()
        else:
            raise Exception("La conexión a la base de datos no está inicializada.")

    @staticmethod
    def return_connection(connection):
        if Database._connection_pool:
            Database._connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        if Database._connection_pool:
            Database._connection_pool.closeall()
