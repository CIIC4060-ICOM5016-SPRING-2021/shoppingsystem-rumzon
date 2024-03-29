import psycopg2
from back_end.config.psycopgConfig import pgconfig


class OrderDAO:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=pgconfig['host'],
            database=pgconfig['dbname'],
            user=pgconfig['user'],
            password=pgconfig['password'],
            port=pgconfig['port']
        )

    def orderTuple(self, u_id, o_id, o_time, o_total):
        items = []
        orderDetails = (u_id, o_id, o_time, o_total, items)
        return orderDetails

    def getAll(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders')
        res = []
        for row in cursor:
            orderDetails = self.orderTuple(row[0], row[1], row[2], row[3])
            res.append(orderDetails)
        cursor.close()
        self.connection.close()
        return res

    def getByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders '
                       'where o_id = %s' %id)
        res = []
        for row in cursor:
            orderDetails = self.orderTuple(row[0], row[1], row[2], row[3])
            res.append(orderDetails)
        return res

    def getByUserID(self, uid):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders '
                       'where u_id = %s' %uid)
        res = []
        for row in cursor:
            orderDetails = self.orderTuple(row[0], row[1], row[2], row[3])
            res.append(orderDetails)
        return res

    def deleteOrder(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM itemsinorder WHERE o_id = %s' % id)
        cursor.execute('DELETE FROM orders WHERE o_id = %s' %id)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def addNewOrder(self, u_id):
        query = 'INSERT INTO orders (u_id) VALUES (%s) RETURNING *'
        cursor = self.connection.cursor()
        cursor.execute(query, [u_id])
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        return res

    def getUserMostExpensiveOrder(self, u_id):
        query = 'SELECT *, ordertotal(o_id) AS o_total FROM orders WHERE orderTotal(o_id) =' \
                '   (SELECT max(o_total) FROM ' \
                '       (SELECT *, orderTotal(o_id) AS o_total FROM orders WHERE u_id = %s) AS T1 ' \
                '   WHERE u_id = %s)'
        cursor = self.connection.cursor()
        cursor.execute(query, (u_id, u_id))
        res = []
        for row in cursor:
            orderDetails = self.orderTuple(row[0], row[1], row[2], row[3])
            res.append(orderDetails)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def getUserLeastExpensiveOrder(self, u_id):
        query = 'SELECT *, ordertotal(o_id) AS o_total FROM orders WHERE orderTotal(o_id) =' \
                '   (SELECT min(o_total) FROM ' \
                '       (SELECT *, orderTotal(o_id) AS o_total FROM orders WHERE u_id = %s) AS T1 ' \
                '   WHERE u_id = %s)'
        cursor = self.connection.cursor()
        cursor.execute(query, (u_id, u_id))
        res = []
        for row in cursor:
            orderDetails = self.orderTuple(row[0], row[1], row[2], row[3])
            res.append(orderDetails)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res