import psycopg2
from config.psycopgConfig import pgconfig


class ItemDAO:
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
        cursor.execute('SELECT * FROM items')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM items '
                       'where item_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def addNewItem(self, i_name, i_category, i_stock, i_price):
        query = 'INSERT INTO items (i_name, i_category, i_stock, i_price) ' \
                'VALUES (%s, %s, %s, %s) RETURNING item_id;'
        cursor = self.connection.cursor()
        cursor.execute(query, (i_name, i_category, i_stock, i_price))
        newItem = cursor.fetchone()
        item_id = newItem[0]
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return item_id

    def deleteItemByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM items WHERE item_id = %s' %id)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def updateItemByID(self, item_id, i_name, i_category, i_stock, i_price):
        query = 'UPDATE items ' \
                'SET i_name = %s, i_category = %s, i_stock = %s, i_price = %s ' \
                'WHERE item_id = %s RETURNING *'
        cursor = self.connection.cursor()
        cursor.execute(query, (i_name, i_category, i_stock, i_price, item_id))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res