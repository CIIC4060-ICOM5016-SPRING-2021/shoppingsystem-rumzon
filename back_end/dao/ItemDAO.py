import psycopg2
from back_end.config.psycopgConfig import pgconfig


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
        cursor.execute('SELECT * FROM items WHERE isActive = True')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getItemsFilterCategory(self, i_category):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM items WHERE i_category = '%s' AND isActive = True " %i_category)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getAllAscendingPrice(self, category):
        cursor = self.connection.cursor()
        if category == 'all':
            query = 'SELECT item_id, i_name, i_category, i_stock, i_price ' \
                    'FROM items WHERE isActive = True ORDER BY i_price ASC'
            cursor.execute(query)
        else:
            query = "SELECT item_id, i_name, i_category, i_stock, i_price FROM items " \
                    "WHERE isActive = True and i_category = '%s' ORDER BY i_price ASC" % category
            cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getAllDescendingPrice(self, category):
        cursor = self.connection.cursor()
        if category == 'all':
            query = 'SELECT item_id, i_name, i_category, i_stock, i_price ' \
                    'FROM items WHERE isActive = True ORDER BY i_price DESC'
            cursor.execute(query)
        else:
            query = "SELECT item_id, i_name, i_category, i_stock, i_price FROM items " \
                    "WHERE isActive = True and i_category = '%s' ORDER BY i_price DESC" % category
            cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getAllAscendingName(self, category):
        cursor = self.connection.cursor()
        if category == 'all':
            query = 'SELECT item_id, i_name, i_category, i_stock, i_price ' \
                    'FROM items WHERE isActive = True ORDER BY i_name ASC'
            cursor.execute(query)
        else:
            query = "SELECT item_id, i_name, i_category, i_stock, i_price FROM items " \
                    "WHERE isActive = True and i_category = '%s' ORDER BY i_name ASC" % category
            cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getAllDescendingName(self, category):
        cursor = self.connection.cursor()
        if category == 'all':
            query = 'SELECT item_id, i_name, i_category, i_stock, i_price ' \
                    'FROM items WHERE isActive = True ORDER BY i_name DESC'
            cursor.execute(query)
        else:
            query = "SELECT item_id, i_name, i_category, i_stock, i_price FROM items " \
                    "WHERE isActive = True and i_category = '%s' ORDER BY i_name DESC" % category
            cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT item_id, i_name, i_category, i_stock, i_price FROM items "
                       "WHERE item_id = '%s' AND isActive = True " %id)
        res = []
        for row in cursor:
            res.append(row)
        # cursor.close()
        # self.connection.close()
        return res

    def isActive(self, item_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT isActive FROM items "
                       "WHERE item_id = %s" %item_id)
        res = []
        for row in cursor:
            res.append(row)
        return res

    def inactiveID(self, i_name, i_category):
        cursor = self.connection.cursor()
        cursor.execute("SELECT item_id FROM items "
                       "WHERE i_name = '%s' AND i_category = '%s' "
                       "AND isActive = False " %(i_name, i_category))
        res = []
        for row in cursor:
            res.append(row)
        return res

    def reactivateItem(self,  item_id, i_price, i_stock):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE ITEMS SET isActive = true, "
                       "i_price = '%s', i_stock = '%s' "
                       "WHERE item_id = %s "
                       "RETURNING item_id, i_name, i_category, i_stock, i_price" %(i_price, i_stock, item_id))
        res = []
        for row in cursor:
            res.append(row)
        return res

    def checkStockByID(self, id, orderAmmount):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, i_stock FROM items '
                       'WHERE item_id = %s AND isActive = True ' %id)
        res = []
        for row in cursor:
            if row[2] < orderAmmount:
                res.append(row)
                res.append(orderAmmount)
        #return item if not enough stock (< orderAmmount), return empty if enough (> orderAmmount)
        return res

    def addNewItem(self, i_name, i_category, i_stock, i_price):
        query = 'INSERT INTO items (i_name, i_category, i_stock, i_price) ' \
                'VALUES (%s, %s, %s, %s) RETURNING item_id, i_name, i_category, i_stock, i_price'
        cursor = self.connection.cursor()
        cursor.execute(query, (i_name, i_category, i_stock, i_price))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def deleteItemByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM itemsincart where item_id = %s' % id)
        cursor.execute('DELETE FROM likes where item_id = %s' % id)
        cursor.execute('UPDATE ITEMS SET isActive = false WHERE item_id = %s' %id)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def updateItemByID(self, item_id, i_name, i_category, i_stock, i_price):
        query = 'UPDATE items ' \
                'SET i_name = %s, i_category = %s, i_stock = %s, i_price = %s ' \
                'WHERE item_id = %s RETURNING item_id, i_name, i_category, i_stock, i_price'
        cursor = self.connection.cursor()
        cursor.execute(query, (i_name, i_category, i_stock, i_price, item_id))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def checkInvalidItem(self, i_name, i_category):
        cursor = self.connection.cursor()
        cursor.execute("SELECT i_name, i_category FROM items "
                       "WHERE i_name = '%s' AND i_category = '%s' AND isActive = True " %(i_name, i_category))
        res = []
        for row in cursor:
            res.append(row)
        return res
