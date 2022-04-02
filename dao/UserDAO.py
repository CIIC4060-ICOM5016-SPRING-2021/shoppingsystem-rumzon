import psycopg2
from config.psycopgConfig import pgconfig


class UserDAO:
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
        cursor.execute('SELECT * FROM users')
        res = []
        for row in cursor:
            res.append(row)
        cursor.close()
        self.connection.close()
        return res

    def getByID(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users '
                       'where u_id = %s' %id)
        res = []
        for row in cursor:
            res.append(row)
        # cursor.close()
        # self.connection.close()
        return res

    def updateUser(self, id, username, u_email, u_password, isAdmin):
        query = 'UPDATE users ' \
                'SET username=%s, u_email=%s, u_password=%s, isAdmin=%s ' \
                'WHERE u_id = %s ' \
                'RETURNING *'
        cursor = self.connection.cursor()
        cursor.execute(query, (username, u_email, u_password, isAdmin, id))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res

    def deleteUser(self, id):
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM itemsinorder where o_id in (select o_id from orders where u_id = %s)' % id)
        cursor.execute('DELETE FROM itemsincart where u_id = %s' % id)
        cursor.execute('DELETE FROM orders where u_id = %s' % id)
        cursor.execute('DELETE FROM likes where u_id = %s' % id)
        cursor.execute('DELETE FROM users where u_id = %s' % id)
        self.connection.commit()
        cursor.close()
        self.connection.close()

    def addNewUser(self, username, u_email, u_password, isAdmin):
        query = 'INSERT INTO users (username, u_email, u_password, isAdmin) ' \
                'VALUES (%s, %s, %s, %s) RETURNING *'
        cursor = self.connection.cursor()
        cursor.execute(query, (username, u_email, u_password, isAdmin))
        res = []
        for row in cursor:
            res.append(row)
        self.connection.commit()
        cursor.close()
        self.connection.close()
        return res
