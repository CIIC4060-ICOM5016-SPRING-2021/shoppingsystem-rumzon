from flask import jsonify
from dao.ItemDAO import ItemDAO

class ItemController:

    def __init__(self):
        self.dao = ItemDAO()

    def dictionary(self, row):
        dic = {}
        dic['item_id'] = row[0]
        dic['i_name'] = row[1]
        dic['i_category'] = row[2]
        dic['i_stock'] = row[3]
        dic['i_price'] = row[4]
        return dic

    def getAll(self):
        daoRes = self.dao.getAll()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Item Table Empty!... or error ocurred'), 405

    def getByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405