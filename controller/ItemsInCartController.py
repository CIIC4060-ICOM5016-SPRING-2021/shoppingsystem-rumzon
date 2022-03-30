from flask import jsonify
from dao.ItemsInCartDAO import ItemsInCartDAO

class ItemsInCartController:

    def __init__(self):
        self.dao = ItemsInCartDAO()

    def dictionary(self, row):
        dic = {}
        dic['item_id'] = row[0]
        dic['u_id'] = row[1]
        dic['c_ammount'] = row[2]
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

    def getUserCartbyID(self, id):
        daoRes = self.dao.getUserCartbyID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("User #%d's cart is empty, or ID Not Found" %id), 405

    def clearUserCartbyID(self, id):
        self.dao.clearUserCartbyID(id)
        return jsonify("User #%s's cart cleared." %id)
