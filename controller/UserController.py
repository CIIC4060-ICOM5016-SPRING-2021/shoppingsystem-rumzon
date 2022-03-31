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
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405

    def deleteUser(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteUser(id)
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405

    def updateUser(self, id, json):
        daoRes = self.dao.getByID(id)
        username = json['username']
        u_email = json['u_email']
        u_password = json['u_password']
        isAdmin = json['isAdmin']
        if daoRes:
            self.dao.updateUser(id, username, u_email, u_password, isAdmin)
            return jsonify(json), 201
        else:
            return jsonify('ID Not Found'), 405

    def addNewUser(self, json):
        username = json['username']
        u_email = json['u_email']
        u_password = json['u_password']
        isAdmin = json['isAdmin']

        u_id = self.dao.addNewUser(username, u_email, u_password, isAdmin)
        json['u_id'] = u_id
        return jsonify(json), 201
