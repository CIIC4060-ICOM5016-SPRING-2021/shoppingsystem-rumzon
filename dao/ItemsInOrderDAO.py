import psycopg2
from config.psycopgConfig import pgconfig


class ItemsInOrderDAO:
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
        cursor.execute('SELECT *, itemTotal(item_id, o_amount) AS i_total FROM itemsinorder')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getOrderItemsByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, itemTotal(item_id, o_amount) AS i_total FROM itemsinorder '
                       'where o_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res