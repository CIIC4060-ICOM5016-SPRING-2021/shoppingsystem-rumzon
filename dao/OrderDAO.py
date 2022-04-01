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
        return res

    def getByUserID(self, uid):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders '
                       'where u_id = %s' %uid)
        res = []
        for row in cursor:
            res.append(row)
        return res

    def deleteOrder(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM itemsinorder WHERE o_id = %s' % id)
        cursor.execute('DELETE FROM orders WHERE o_id = %s' %id)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def updateOrder(self, o_id, u_id):
        query = 'UPDATE orders SET u_id=%s WHERE o_id = %s RETURNING *, orderTotal(o_id) AS o_total '
        cursor = self.connection.cursor()
        cursor.execute(query, (u_id, o_id))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def addNewOrder(self, u_id):
        query = 'INSERT INTO orders (u_id) VALUES (%s) RETURNING o_id'
        cursor = self.connection.cursor()
        cursor.execute(query, [u_id])
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res
