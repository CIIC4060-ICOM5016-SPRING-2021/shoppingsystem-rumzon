import psycopg2
from config.psycopgConfig import pgconfig


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

    def getUserLikesByUserID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM likes '
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