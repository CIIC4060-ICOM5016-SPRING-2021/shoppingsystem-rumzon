import psycopg2
from back_end.config.psycopgConfig import pgconfig


class LikesDAO:
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
        cursor.execute('SELECT * FROM likes')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getLikeCount(self):
        query = 'SELECT item_id, i_name, i_category, count(u_id) AS like_count FROM likes natural inner join items ' \
                'GROUP BY item_id, i_name, i_category ORDER BY like_count DESC;'
        cursor = self.connection.cursor()
        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row)
        return res

    def getUserLikesByUserID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT item_id, i_name, i_category, i_price FROM likes natural inner join items '
                       'where u_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getItemLikesByItemID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM likes '
                       'where item_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def addLike(self, u_id, item_id):
        recordFound = self.isInRecord(u_id, item_id)
        if recordFound:
            return
        query = 'INSERT INTO likes (u_id, item_id) VALUES (%s, %s) RETURNING *'
        cursor = self.connection.cursor()
        cursor.execute(query, [u_id, item_id])
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def deleteLike(self, u_id, item_id):
        recordFound = self.isInRecord(u_id, item_id)
        if not recordFound:
            return
        query = 'DELETE FROM likes where u_id = %s and item_id = %s'
        cursor = self.connection.cursor()
        cursor.execute(query, [u_id, item_id])
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return recordFound


    def isInRecord(self, u_id, item_id):
        query = 'SELECT item_id, u_id FROM likes where u_id = %s and item_id = %s'
        cursor = self.connection.cursor()
        cursor.execute(query, [u_id, item_id])
        res = []
        for row in cursor:
            res.append(row)
        return res