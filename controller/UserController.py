from flask import jsonify
from dao.UserDAO import UserDAO

class UserController:

    def __init__(self):
        self.dao = UserDAO()

    def dictionary(self, row):
        dic = {}
        dic['u_id'] = row[0]
        dic['username'] = row[1]
        dic['u_email'] = row[2]
        dic['u_password'] = row[3]
        dic['isAdmin'] = row[4]
        return dic

    def getAll(self):
        daoRes = self.dao.getAll()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('User Table Empty!... or error ocurred'), 405

    def getByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 405

    def getUserDict(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return self.dictionary(daoRes[0])
        else:
            return {}

    def deleteUser(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteUser(id)
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def updateUser(self, id, reqjson):
        oldjson = self.getUserDict(id)

        if oldjson:
            username = oldjson['username']
            u_email = oldjson['u_email']
            u_password = oldjson['u_password']

            if reqjson['username'] != '':
                username = reqjson['username']
            if reqjson['u_email'] != '':
                u_email = reqjson['u_email']
            if reqjson['u_password'] != '':
                u_password = reqjson['u_password']
            if type(reqjson['isAdmin']) is str:
                if reqjson['isAdmin'].lower() == '':
                    isAdmin = oldjson['isAdmin']
                elif reqjson['isAdmin'].lower() == 'true':
                    isAdmin = 'true'
                else:
                    isAdmin = 'false'
            else:
                isAdmin = reqjson['isAdmin']

            daoRes = self.dao.updateUser(id, username, u_email, u_password, isAdmin)
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def addNewUser(self, json):
        if json['username'] == '':
            return jsonify('Enter Username'), 418
        if json['u_email'] == '':
            return jsonify('Enter Email'), 418
        if json['u_password'] == '':
            return jsonify('Enter Password'), 418

        username = json['username']
        u_email = json['u_email']
        u_password = json['u_password']
        isAdmin = json['isAdmin']

        daoRes = self.dao.addNewUser(username, u_email, u_password, isAdmin)
        if daoRes:
            res = []
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res), 201
        else:
            return jsonify('Error creating user'), 400
