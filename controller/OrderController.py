from flask import jsonify
from dao.OrderDAO import OrderDAO
from dao.UserDAO import UserDAO
from dao.ItemsInOrderDAO import ItemsInOrderDAO

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

    def getByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result), 200
        else:
            return jsonify('ID Not Found'), 404

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

    def getAllByUserID(self, uid):
        daoRes = self.dao.getByUserID(uid)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
                itemRes = ItemsInOrderDAO().getItemsFromOrder(row[1])
                for item in itemRes:
                    row[4].append(self.ItemsDict(item))
            return jsonify(result), 200
        else:
            return jsonify('ID Not Found'), 404

    def deleteOrder(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteOrder(id)
            dicRes = {}
            dicRes['User ID'] = daoRes[0][0]
            dicRes['Order ID'] = daoRes[0][1]
            dicRes['Order Time'] = daoRes[0][2]
            return jsonify(dicRes), 200
        else:
            return jsonify('ID Not Found'), 405

    def updateOrder(self, o_id, reqjson):
        userIDValid = UserDAO().getByID(reqjson['u_id'])
        if not userIDValid:
            return jsonify('Invalid User ID'), 400

        oldjson = self.getDictByID(o_id)
        if oldjson:
            u_id = oldjson['u_id']
            if reqjson['u_id'] != '':
                u_id = reqjson['u_id']

            daoRes = self.dao.updateOrder(o_id, u_id)
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def addNewOrder(self, reqjson):
        userIDValid = UserDAO().getByID(reqjson['u_id'])
        if not userIDValid:
            return jsonify('Invalid User ID'), 400

        u_id = reqjson['u_id']
        daoRes = self.dao.addNewOrder(u_id)
        if daoRes:
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

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
            return jsonify('User #%s does not have purchases! ...or error ocurred' %u_id), 404

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
            return jsonify('User #%s does not have purchases! ...or error ocurred' %u_id), 404