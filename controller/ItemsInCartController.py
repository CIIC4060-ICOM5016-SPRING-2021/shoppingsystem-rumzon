from flask import jsonify
from dao.ItemsInCartDAO import ItemsInCartDAO
from dao.OrderDAO import OrderDAO

class ItemsInCartController:

    def __init__(self):
        self.dao = ItemsInCartDAO()
        self.order = OrderDAO()

    def dictionary(self, row):
        dic = {}
        dic['item_id'] = row[0]
        dic['u_id'] = row[1]
        dic['c_amount'] = row[2]
        dic['i_total'] = row[3]
        return dic

    def getAll(self):
        daoRes = self.dao.getAll()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Cart Table Empty!... or error ocurred'), 405

    def getUserCartByID(self, id):
        daoRes = self.dao.getUserCartByID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("User #%d's cart is empty, or ID Not Found" %id), 405

    def getUserCartTotalByID(self, id):
        daoRes = self.dao.getUserCartTotalByID(id)
        if daoRes:
            dic = {}
            for row in daoRes:
                if row[1] is None:
                    return jsonify("User #%s Cart Empty" % row[0]), 200
                dic['u_id'] = row[0]
                dic['c_total'] = row[1]
            return jsonify(dic), 200
        else:
            return jsonify("ID Not Found" %id), 405

    def addToCart(self, json):
        item_id = json['item_id']
        u_id = json['u_id']
        c_amount = json['c_amount']

        daoRes = self.dao.addItemToCart(item_id, u_id, c_amount)
        if daoRes:
            res = []
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res)
        else:
            return jsonify('Error adding to cart'), 400

    def updateFromCart(self, json):
        item_id = json['item_id']
        u_id = json['u_id']
        c_amount = json['c_amount']

        daoRes = self.dao.updateFromCart(item_id, u_id, c_amount)
        if daoRes:
            res = []
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res)
        else:
            return jsonify('Error updating cart'), 400

    def deleteItemInCart(self, json):
        item_id = json['item_id']
        u_id = json['u_id']
        daoRes = self.dao.deleteItemInCart(item_id, u_id)
        if daoRes:
            res = []
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res)
        else:
            return jsonify('Error deleting item in cart'), 400

    def clearUserCartByID(self, id):
        self.dao.clearUserCartByID(id)
        return jsonify("User #%s's cart cleared." %id)

    def buyAllFromCart(self, u_id):
        orderId = self.order.addNewOrder(u_id)
        daoRes = self.dao.getUserCartByID(u_id)
        if orderId and daoRes:
            result = []
            for row in daoRes:
                self.dao.buyItemFromCart(row[0], orderId, row[2])
                result.append(self.dictionary(row))
            self.dao.clearUserCartByID(u_id)
            return jsonify(result)
        else:
            return jsonify("User #%d's cart is empty, or ID Not Found" % u_id), 405
