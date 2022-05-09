from flask import jsonify
from back_end.dao.UserDAO import UserDAO
import re

class UserController:

    def __init__(self):
        self.dao = UserDAO()

    def dictionary(self, row):
        dic = {}
        dic['User ID'] = row[0]
        dic['Username'] = row[1]
        dic['Email'] = row[2]
        dic['Password'] = row[3]
        dic['is Admin'] = row[4]
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

    def getByID(self, json):
        daoRes = self.dao.getByID(json['u_id'])
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

    def isAdmin(self,id):
        daoRes = self.dao.isAdmin(id)
        if daoRes:
            for row in daoRes:
                if row[0] == True:
                    return 1  # user is admin
                else:
                    return 0  # user is not admin
        else:
            return -1  # user id not found or error

    def deleteUser(self, json):
        daoRes = self.dao.getByID(json['u_id'])
        if daoRes:
            self.dao.deleteUser(json['u_id'])
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def updateUser(self, reqjson):
        oldjson = self.getUserDict(reqjson['u_id'])

        if oldjson:
            username = oldjson['Username']
            u_email = oldjson['Email']
            u_password = oldjson['Password']

            emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

            if reqjson['username'] != reqjson['username'].replace(' ', ''):
                return jsonify('Username must not have spaces'), 400
            if not (re.search(emailRegex, reqjson['u_email'])) and reqjson['u_email'] != '':
                return jsonify('Enter Valid Email'), 400
            if not isinstance(reqjson['isAdmin'], bool) and reqjson['isAdmin'] != '':
                return jsonify('isAdmin must be Boolean'), 400

            if reqjson['username'].replace(' ', '') != '' and reqjson['username'] != oldjson['Username']:
                userInvalid = self.checkUsername(reqjson['username'])
                if userInvalid:
                    return jsonify('Username already taken'), 400
                else:
                    username = reqjson['username']

            if reqjson['u_email'].replace(' ', '') != '' and reqjson['u_email'] != oldjson['Email']:
                emailInvalid = self.checkEmail(reqjson['u_email'])
                if emailInvalid:
                    return jsonify('Email already taken'), 400
                else:
                    u_email = reqjson['u_email']

            if reqjson['u_password'] != '':
                u_password = reqjson['u_password']
            if type(reqjson['isAdmin']) is str and reqjson['isAdmin'] == '':
                    isAdmin = oldjson['is Admin']
            else:
                isAdmin = reqjson['isAdmin']

            daoRes = self.dao.updateUser(reqjson['u_id'], username, u_email, u_password, isAdmin)
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def addNewUser(self, json):
        res = []
        try:
            if json['username'] == '':
                return jsonify('Enter Username'), 400
            if json['u_email'] == '':
                return jsonify('Enter Email'), 400
            if json['u_password'] == '':
                return jsonify('Enter Password'), 400
            if not isinstance(json['isAdmin'], bool):
                return jsonify('isAdmin must be Boolean'), 400
        except:
            return jsonify('Bad Json'), 400
        emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if json['username'] != json['username'].replace(' ', ''):
            return jsonify('Username must not have spaces'), 400
        if not (re.search(emailRegex, json['u_email'])):
            return jsonify('Enter Valid Email'), 400
        userInvalid = self.checkUsername(json['username'])
        if userInvalid:
            return jsonify('Username already taken'), 400
        emailInvalid = self.checkEmail(json['u_email'])
        if emailInvalid:
            return jsonify('Email already taken'), 400

        username = json['username']
        u_email = json['u_email']
        u_password = json['u_password']
        isAdmin = json['isAdmin']

        daoRes = self.dao.addNewUser(username, u_email, u_password, isAdmin)
        if daoRes:
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res), 201
        else:
            return jsonify('Error creating user'), 500

    def login(self, json):
        if json['user'] == "":
            return ("Enter Username or Email"), 400
        if json['password'] == "":
            return ("Enter Password"), 400

        emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(emailRegex, json['user'])):
            daoRes = self.dao.loginEmail(json['user'], json['password'])
        else:
            daoRes= self.dao.loginUsername(json['user'], json['password'])
        if daoRes:
            dic = {}
            for row in daoRes:
                dic['User ID'] = row[0]
                dic['Username'] = row[1]
                dic['IsAdmin'] = row[2]
            return jsonify(dic), 200
        else:
            return ("User or Password incorrect"), 404


    def checkUsername(self, username):
        usernameRes = self.dao.checkUsername(username)
        res = []
        if usernameRes:
            for row in usernameRes:
                res.append(row)
        return res #return already taken username or empty if valid

    def checkEmail(self, email):
        emailRes = self.dao.checkEmail(email)
        res = []
        if emailRes:
            for row in emailRes:
                res.append(row)
        return res #return already taken email or empty if valid