import psycopg2
from config.psycopgConfig import pgconfig


class OrderDAO:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=pgconfig['host'],
            database=pgconfig['dbname'],
            user=pgconfig['user'],
            password=pgconfig['password'],
            port=pgconfig['port']
        )

    def getAll(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders '
                       'where o_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res