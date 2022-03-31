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
        cursor.execute('SELECT *, itemTotal(item_id, c_ammount) AS i_total FROM itemsincart')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserCartByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT *, itemTotal(item_id, c_ammount) AS i_total FROM itemsincart '
                       'where u_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        # cursor.close()
        # self.connection.close()
        return res

    def clearUserCartByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM itemsincart WHERE u_id = %s' %id)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def buyItemFromCart(self, item_id, o_id, o_ammount):
        query = 'INSERT INTO itemsinorder (item_id, o_id, o_ammount)' \
                    'VALUES (%s, %s, %s);'
        cursor = self.connection.cursor()
        cursor.execute(query, (item_id, o_id, o_ammount))
        self.connection.commit()
        # cursor.close()
        # self.connection.close()
