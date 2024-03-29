from flask import jsonify

from back_end.controller.ItemsInOrderController import ItemsInOrderController
from back_end.controller.OrderController import OrderController
from back_end.dao.ItemsInCartDAO import ItemsInCartDAO
from back_end.dao.ItemDAO import ItemDAO
from back_end.dao.ItemsInOrderDAO import ItemsInOrderDAO
from back_end.dao.OrderDAO import OrderDAO
from back_end.dao.UserDAO import UserDAO


class ItemsInCartController:

    def __init__(self):
        self.dao = ItemsInCartDAO()

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
            return jsonify('Cart Table Empty!... or error ocurred'), 404

    def getUserCartByID(self, json):
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('Invalid User ID'), 400
        daoRes = self.dao.getUserCartByID(json['u_id'])
        if daoRes:
            cartItems = []
            totalRes = self.dao.getUserCartTotalByID(json['u_id'])
            resDic = {}
            resDic["User ID"] = totalRes[0][0]
            resDic["Cart Total"] = totalRes[0][1]
            for row in daoRes:
                itemDic = {}
                itemDic["Item ID"] = row[0]
                itemDic["Name"] = row[1]
                itemDic["Category"] = row[2]
                itemDic["Amount"] = row[3]
                itemDic["Price"] = row[4]
                itemDic["Item Total"] = row[5]
                cartItems.append(itemDic)
            resDic["Cart Items"] = cartItems
            return jsonify(resDic)
        else:
            return jsonify("User #%d's cart is empty" %json['u_id']), 404

    def getUserCartTotalByID(self, json):
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('User ID not found'), 404
        daoRes = self.dao.getUserCartTotalByID(json['u_id'])
        if daoRes:
            dic = {}
            for row in daoRes:
                if row[1] is None:
                    return jsonify("User #%s Cart Empty" % row[0]), 200
                dic['User ID'] = row[0]
                dic['Cart Total'] = row[1]
            return jsonify(dic), 200
        else:
            return jsonify("User #%d's cart is empty" % json['u_id']), 404

    def addToCart(self, json):
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('User ID not found'), 404
        itemIDValid = ItemDAO().getByID(json['item_id'])
        if not itemIDValid:
            return jsonify('Item ID not found'), 404
        item_id = json['item_id']
        u_id = json['u_id']
        ammountInCart = self.verifyItemInCart(item_id, u_id)

        c_amount = json['c_amount']
        if ammountInCart != 0 and ammountInCart[0] > 0 and (c_amount+ammountInCart[0] > 0):
            daoRes = self.dao.updateFromCart(item_id, u_id, (c_amount+ammountInCart[0]))
        else:
            daoRes = self.dao.addItemToCart(item_id, u_id, c_amount)
        if daoRes:
            res = []
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res)
        else:
            return jsonify('Error adding to cart'), 400

    def updateFromCart(self, json):
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('User ID not found'), 404
        itemIDValid = ItemDAO().getByID(json['item_id'])
        if not itemIDValid:
            return jsonify('Item ID not found'), 404
        item_id = json['item_id']
        u_id = json['u_id']
        itemInCart = self.verifyItemInCart(item_id, u_id)
        if itemInCart == 0:
            return jsonify("Item %s not in User %s cart" % (item_id, u_id)), 400
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
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('User ID not found'), 404
        itemIDValid = ItemDAO().getByID(json['item_id'])
        if not itemIDValid:
            return jsonify('Item ID not found'), 404
        item_id = json['item_id']
        u_id = json['u_id']
        itemInCart = self.verifyItemInCart(item_id, u_id)
        if itemInCart == 0:
            return jsonify("Item %s not in User %s cart" % (item_id, u_id)), 400

        daoRes = self.dao.deleteItemInCart(item_id, u_id)
        if daoRes:
            res = []
            for row in daoRes:
                res.append(self.dictionary(row))
            return jsonify(res)
        else:
            return jsonify('Error deleting item in cart'), 400

    def clearUserCartByID(self, json):
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('User ID not found'), 404
        self.dao.clearUserCartByID(json['u_id'])
        return jsonify("User #%s's cart cleared." % json['u_id'])

    def buyAllFromCart(self, json):
        userIDValid = UserDAO().getByID(json['u_id'])
        if not userIDValid:
            return jsonify('User ID not found'), 404
        daoRes = self.dao.getUserCartByID(json['u_id'])
        #check if enough in stock for each item in cart
        if daoRes:
            understockedItems = []
            for row in daoRes:
                print(row[0])
                print(row[3])
                stockRes = ItemDAO().checkStockByID(row[0], row[3])
                if stockRes:
                    itemDic = {}
                    itemDic['Item ID'] = stockRes[0][0]
                    itemDic['Item Name'] = stockRes[0][1]
                    itemDic['Stock'] = stockRes[0][2]
                    itemDic['Cart Ammount'] = stockRes[1]
                    itemDic['Error'] = 'Not enough %s in stock' %itemDic['Item Name']
                    understockedItems.append(itemDic)
            if understockedItems:
                return jsonify(understockedItems), 403

        #make purchase if all items good in stock
        orderRes = OrderDAO().addNewOrder(json['u_id'])
        if orderRes and daoRes:
            itemsInOrderDao = ItemsInOrderDAO()
            o_id = orderRes[0][1]
            result = []
            for row in daoRes:
                itemsInOrderDao.buyItemFromCart(row[0], o_id, row[3])
                result.append(self.dictionary(row))
            self.dao.clearUserCartByID(json['u_id'])
            return OrderController().getByID(o_id)
        else:
            return jsonify("User #%d's cart is empty" % json['u_id']), 405

    def verifyItemInCart(self, item_id, u_id):
        userIDValid = UserDAO().getByID(u_id)
        if not userIDValid:
            return jsonify('User ID not found')
        itemIDValid = ItemDAO().getByID(item_id)
        if not itemIDValid:
            return jsonify('Item ID not found')

        print(item_id)
        print(u_id)
        daoRes = self.dao.verifyItemInCart(item_id, u_id)

        if daoRes:
            return daoRes[0]
        else:
            return 0