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

    def getItemsFromOrder(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, i_category, o_amount, i_total '
                       'FROM itemsinorder NATURAL INNER JOIN items '
                       'WHERE o_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        # cursor.close()
        # self.connection.close()
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

    def getItemsPurchaseCount(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, purchasecount(item_id) AS purchase_count '
                       'FROM itemsinorder natural inner join items '
                       'GROUP BY item_id, i_name '
                       'ORDER BY purchase_count DESC '
                       'LIMIT 20')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getActiveItemsPurchaseCount(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, purchasecount(item_id) AS purchase_count '
                       'FROM itemsinorder natural inner join items '
                       'WHERE isActive = True ' 
                       'GROUP BY item_id, i_name '
                       'ORDER BY purchase_count DESC '
                       'LIMIT 20')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getCategoryPurchaseCount(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT i_category, categorypurcount(i_category) AS purchase_count '
                       'FROM itemsinorder natural inner join items '
                       'GROUP BY i_category '
                       'ORDER BY purchase_count DESC')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getActiveCategoryPurchaseCount(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT i_category, activecategorypurcount(i_category) AS purchase_count '
                       'FROM itemsinorder natural inner join items '
                       'WHERE isActive = True '
                       'GROUP BY i_category '
                       'ORDER BY purchase_count DESC')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserItemsPurchaseCount(self, u_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, purchasecount(item_id) AS purchase_count '
                       'FROM itemsinorder NATURAL INNER JOIN items NATURAL INNER JOIN orders '
                       'WHERE u_id = %s '
                       'GROUP BY item_id, i_name '
                       'ORDER BY purchase_count DESC '
                       'LIMIT 20' % u_id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserActiveItemsPurchaseCount(self, u_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, purchasecount(item_id) AS purchase_count '
                       'FROM itemsinorder NATURAL INNER JOIN items NATURAL INNER JOIN orders '
                       'WHERE u_id = %s '
                       'AND isActive = True '
                       'GROUP BY item_id, i_name '
                       'ORDER BY purchase_count DESC '
                       'LIMIT 20' % u_id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserCategoryPurchaseCount(self, u_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT i_category, categorypurcount(i_category) AS purchase_count '
                       'FROM itemsinorder NATURAL INNER JOIN items NATURAL INNER JOIN orders '
                       'WHERE u_id = %s '
                       'GROUP BY i_category '
                       'ORDER BY purchase_count DESC' % u_id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserActiveCategoryPurchaseCount(self, u_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT i_category, activecategorypurcount(i_category) AS purchase_count '
                       'FROM itemsinorder NATURAL INNER JOIN items NATURAL INNER JOIN orders '
                       'WHERE u_id = %s '
                       'AND isActive = True '
                       'GROUP BY i_category '
                       'ORDER BY purchase_count DESC' % u_id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserMostExpensiveItemPurchase(self, u_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT o_id, item_id, i_name, i_category, o_amount, i_total '
                       'FROM itemsinorder NATURAL INNER JOIN items NATURAL INNER JOIN orders '
                       'WHERE i_total = (SELECT max(i_total) FROM itemsinorder NATURAL INNER JOIN orders WHERE u_id = %s) '
                       'AND u_id = %s' % (u_id, u_id))
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getUserLeastExpensiveItemPurchase(self, u_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT o_id, item_id, i_name, i_category, o_amount, i_total '
                       'FROM itemsinorder NATURAL INNER JOIN items NATURAL INNER JOIN orders '
                       'WHERE i_total = (SELECT min(i_total) FROM itemsinorder NATURAL INNER JOIN orders WHERE u_id = %s) '
                       'AND u_id = %s' % (u_id, u_id))
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res