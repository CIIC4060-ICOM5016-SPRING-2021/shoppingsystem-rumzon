from flask import jsonify
import json
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

    def getDictByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return self.dictionary(daoRes[0])
        else:
            return {}

    def addNewItem(self, json):
        i_name = json['i_name']
        i_category = json['i_category']
        i_stock = json['i_stock']
        i_price = json['i_price']

        item_id = self.dao.addNewItem(i_name, i_category, i_stock, i_price)
        json['item_id'] = item_id
        return jsonify(json), 201

    def deleteItem(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteItemByID(id)
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405

    def updateItem(self, id, reqjson):

        oldjson = self.getDictByID(id)
        i_name = oldjson['i_name']
        i_category = oldjson['i_category']
        i_stock = oldjson['i_stock']
        i_price = oldjson['i_price']

        if reqjson['i_name'] != '':
            i_name = reqjson['i_name']
        if reqjson['i_category'] != '':
            i_category = reqjson['i_category']
        if reqjson['i_stock'] != '':
            i_stock = reqjson['i_stock']
        if reqjson['i_price'] != '':
            i_price = reqjson['i_price']

        daoRes = self.dao.updateItemByID(id, i_name, i_category, i_stock, i_price)
        if daoRes:
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('Error editing item with ID %d' %id), 405