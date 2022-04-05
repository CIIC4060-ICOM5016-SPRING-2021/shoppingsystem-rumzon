from flask import jsonify
from dao.ItemsInCartDAO import ItemsInCartDAO
from dao.ItemDAO import ItemDAO
from dao.ItemsInOrderDAO import ItemsInOrderDAO
from dao.OrderDAO import OrderDAO

class ItemsInCartController:

    def __init__(self):
        self.dao = ItemsInCartDAO()
        self.order = OrderDAO()

    def dictionary(self, row):
        dic = {}
        dic['Item ID'] = row[0]
        dic['User ID'] = row[1]
        dic['Cart Amount'] = row[2]
        dic['Item Total'] = row[3]
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
                dic['User ID'] = row[0]
                dic['Cart Total'] = row[1]
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
        daoRes = self.dao.getUserCartByID(u_id)
        #check if enough in stock for each item in cart
        if daoRes:
            understockedItems = []
            for row in daoRes:
                stockRes = ItemDAO().checkStockByID(row[0], row[2])
                if stockRes:
                    print(stockRes[0][0])
                    print(stockRes[0][1])
                    print(stockRes[0][2])
                    print(stockRes[1])
                    itemDic = {}
                    itemDic['Item ID'] = stockRes[0][0]
                    itemDic['Item Name'] = stockRes[0][1]
                    itemDic['Stock'] = stockRes[0][2]
                    itemDic['Cart Ammount'] = stockRes[1]
                    itemDic['Error'] = 'Not enough %s in stock' %itemDic['Item Name']
                    understockedItems.append(itemDic)
            if understockedItems:
                return jsonify(understockedItems), 400

        #make purchase if all items good in stock
        orderRes = self.order.addNewOrder(u_id)
        if orderRes and daoRes:
            itemsInOrderDAO = ItemsInOrderDAO()
            o_id = orderRes[0][1]
            result = []
            for row in daoRes:
                itemsInOrderDAO.buyItemFromCart(row[0], o_id, row[2])
                result.append(self.dictionary(row))
            self.dao.clearUserCartByID(u_id)
            return jsonify(result)
        else:
            return jsonify("User #%d's cart is empty, or ID Not Found" % u_id), 405