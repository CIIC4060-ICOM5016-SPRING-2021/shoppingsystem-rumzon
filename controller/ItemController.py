from flask import jsonify
import json
from dao.ItemDAO import ItemDAO

class ItemController:

    def __init__(self):
        self.dao = ItemDAO()

    def dictionary(self, row):
        dic = {}
        dic['Item ID'] = row[0]
        dic['Item Name'] = row[1]
        dic['Category'] = row[2]
        dic['Stock'] = row[3]
        dic['Price'] = row[4]
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

    def getItemsFilterCategory(self, i_category):
        daoRes = self.dao.getItemsFilterCategory(i_category)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Item Table Empty!... or error ocurred'), 405

    def getAllAscendingPrice(self):
        daoRes = self.dao.getAllAscendingPrice()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Item Table Empty!... or error ocurred'), 405

    def getAllDescendingPrice(self):
        daoRes = self.dao.getAllDescendingPrice()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Item Table Empty!... or error ocurred'), 405

    def getAllAscendingName(self):
        daoRes = self.dao.getAllAscendingName()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Item Table Empty!... or error ocurred'), 405

    def getAllDescendingName(self):
        daoRes = self.dao.getAllDescendingName()
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

    def deleteItem(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteItemByID(id)
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405

    def addNewItem(self, json):
        i_name = json['i_name']
        i_category = json['i_category']
        i_stock = json['i_stock']
        i_price = json['i_price']

        daoRes = self.dao.addNewItem(i_name, i_category, i_stock, i_price)
        if daoRes:
            return self.dictionary(daoRes[0])
        else:
            return jsonify('Error creating Item'), 405

    def updateItem(self, id, reqjson):
        oldjson = self.getDictByID(id)

        if oldjson:
            i_name = oldjson['Item Name']
            i_category = oldjson['Category']
            i_stock = oldjson['Stock']
            i_price = oldjson['Price']

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
            return jsonify('ID %d not found' %id), 404
