from flask import jsonify
from dao.ItemsInOrderDAO import ItemsInOrderDAO

class ItemsInOrderController:

    def __init__(self):
        self.dao = ItemsInOrderDAO()

    def dictionary(self, row):
        dic = {}
        dic['item_id'] = row[0]
        dic['o_id'] = row[1]
        dic['o_ammount'] = row[2]
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
            return jsonify('Items in Orders Table Empty!... or error ocurred'), 405

    def getOrderItemsByID(self, id):
        daoRes = self.dao.getOrderItemsByID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("Order #%d is empty, or ID Not Found" %id), 405