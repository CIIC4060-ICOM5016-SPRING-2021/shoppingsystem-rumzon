import psycopg2
from config.psycopgConfig import pgconfig


class ItemsInCartDAO:
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
        cursor.execute('SELECT *, itemTotal(item_id, c_amount) AS i_total FROM itemsincart')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserCartByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, itemTotal(item_id, c_amount) AS i_total FROM itemsincart '
                       'where u_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        # cursor.close()
        # self.connection.close()
        return res

    def getUserCartTotalByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT u_id, carttotal(u_id) from users where u_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        # cursor.close()
        # self.connection.close()
        return res

    def addItemToCart(self, item_id, u_id, c_amount):
        query = 'INSERT INTO itemsincart (item_id, u_id, c_amount) ' \
                       'VALUES (%s, %s, %s) RETURNING *, itemTotal(item_id, c_amount) AS i_total'
        cursor = self.connection.cursor()
        cursor.execute(query, (item_id, u_id, c_amount))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        return res

    def updateFromCart(self, item_id, u_id, c_amount):
        query = 'UPDATE itemsincart SET c_amount = %s WHERE item_id = %s AND u_id = %s' \
                ' RETURNING *, itemTotal(item_id, c_amount) AS i_total'
        cursor = self.connection.cursor()
        cursor.execute(query, (c_amount, item_id, u_id))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        return res

    def deleteItemInCart(self, item_id, u_id):
        query = 'DELETE FROM itemsincart WHERE item_id = %s AND u_id = %s ' \
                'RETURNING *, itemTotal(item_id, c_amount) AS i_total'
        cursor = self.connection.cursor()
        cursor.execute(query, (item_id, u_id))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def clearUserCartByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM itemsincart WHERE u_id = %s' %id)
        self.connection.commit()
        cursor.close()
        self.connection.close()


