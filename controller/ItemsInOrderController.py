from flask import jsonify
from dao.ItemsInOrderDAO import ItemsInOrderDAO

class ItemsInOrderController:

    def __init__(self):
        self.dao = ItemsInOrderDAO()

    def dictionary(self, row):
        dic = {}
        dic['Item ID'] = row[0]
        dic['Order ID'] = row[1]
        dic['Amount'] = row[2]
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
            return jsonify('Items in Orders Table Empty!... or error ocurred'), 405

    def getOrderItemsByOrderID(self, id):
        daoRes = self.dao.getOrderItemsByOrderID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("Order #%d is empty, or ID Not Found" %id), 405