from flask import jsonify

from back_end.controller.UserController import UserController
from back_end.dao.OrderDAO import OrderDAO
from back_end.dao.UserDAO import UserDAO
from back_end.dao.ItemsInOrderDAO import ItemsInOrderDAO

class OrderController:

    def __init__(self):
        self.dao = OrderDAO()

    def dictionary(self, row):
        dic = {}
        dic['User ID'] = row[0]
        dic['Order ID'] = row[1]
        dic['Order Time'] = row[2]
        dic['Order Total'] = row[3]
        dic['Items in Order'] = row[4]
        return dic

    def ItemsDict(self, row):
        dic = {}
        dic['Item ID'] = row[0]
        dic['Item Name'] = row[1]
        dic['Category'] = row[2]
        dic['Amount'] = row[3]
        dic['Item Total'] = row[4]
        return dic

    def getAll(self):
        daoRes = self.dao.getAll()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result), 200
        else:
            return jsonify('Order Table Empty!... or error ocurred'), 400

    def getByID(self, o_id):
        daoRes = self.dao.getByID(o_id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result), 200
        else:
            return jsonify('Order ID Not Found'), 404

    def getDictByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return self.dictionary(daoRes[0])
        else:
            return {}

    def getAllByUserID(self, json):
        userIDValid = UserDAO().getByID(json["u_id"])
        if not userIDValid:
            return jsonify('User ID not found'), 404

        daoRes = self.dao.getByUserID(json["u_id"])
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result), 200
        else:
            return jsonify('User #%s does not have purchases!' % json["u_id"]), 404

    def deleteOrder(self, json):
        if not isinstance(json['admin_id'], int):
            return jsonify("Enter valid User ID integer"), 400

        isAdmin = UserController().isAdmin(json['admin_id'])
        if isAdmin == 0:
            return jsonify('User %d does not have admin privileges' % json['admin_id']), 403
        elif isAdmin == -1:
            return jsonify('User %d not found' % json['admin_id']), 404

        daoRes = self.dao.getByID(json['o_id'])
        if daoRes:
            self.dao.deleteOrder(json['o_id'])
            dicRes = {}
            dicRes['User ID'] = daoRes[0][0]
            dicRes['Order ID'] = daoRes[0][1]
            dicRes['Order Time'] = daoRes[0][2]
            return jsonify(dicRes), 200
        else:
            return jsonify('Order ID Not Found'), 404

    def addNewOrder(self, reqjson):
        userIDValid = UserDAO().getByID(reqjson['u_id'])
        if not userIDValid:
            return jsonify('Invalid User ID'), 400
        u_id = reqjson['u_id']
        daoRes = self.dao.addNewOrder(u_id)
        if daoRes:
            dicRes = {}
            dicRes['User ID'] = daoRes[0][0]
            dicRes['Order ID'] = daoRes[0][1]
            dicRes['Order Time'] = daoRes[0][2]
            return jsonify(dicRes), 200
        else:
            return jsonify('Error creating order'), 500

    def getUserMostExpensiveOrder(self, u_id):
        daoRes = self.dao.getUserMostExpensiveOrder(u_id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result)
        else:
            return jsonify('User #%s does not have purchases!' %u_id), 404

    def getUserLeastExpensiveOrder(self, u_id):
        daoRes = self.dao.getUserLeastExpensiveOrder(u_id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result)
        else:
            return jsonify('User #%s does not have purchases!' %u_id), 404