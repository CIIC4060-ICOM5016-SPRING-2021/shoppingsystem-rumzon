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
        cursor.execute('SELECT * FROM itemsinorder')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getOrderItemsByOrderID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM itemsinorder '
                       'where o_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def buyItemFromCart(self, item_id, o_id, o_amount):
        query = 'INSERT INTO itemsinorder (item_id, o_id, o_amount, i_total) ' \
                'VALUES (%s, %s, %s, itemTotal(%s, %s)) RETURNING *'
        cursor = self.connection.cursor()
        cursor.execute(query, (item_id, o_id, o_amount, item_id, o_amount))
        query2 = 'UPDATE items SET i_stock = (i_stock - %s) WHERE item_id = %s'
        cursor = self.connection.cursor()
        cursor.execute(query2, (o_amount, item_id))
        self.connection.commit()
        # cursor.close()
        # self.connection.close()