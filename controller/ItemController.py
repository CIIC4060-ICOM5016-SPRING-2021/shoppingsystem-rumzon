from flask import jsonify
import json
from dao.ItemDAO import ItemDAO

class ItemController:

    category_list = ['food','clothes','electronics','furniture',
                     'household','kitchenware','medicine','pets',
                     'sports','supplies','toys']

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

        if json['i_name'].replace(' ', '') == '':
            return jsonify('Enter Item Name'), 400
        if json['i_category'] == '':
            return jsonify('Enter Category'), 400
        if not isinstance(json['i_stock'], int) or json['i_stock'] <= 0:
            return jsonify('Stock must be Integer greater than 0'), 400
        if json['i_stock'] > 999999999:
            return jsonify('Stock cannot be greater than 999,999,999'), 400
        if (not isinstance(json['i_price'], float) and not isinstance(json['i_price'], int)) or json['i_price'] < 0:
            return jsonify('Enter Valid Price'), 400

        invalidItem = self.checkInvalidItem(json['i_name'], json['i_category'])
        if invalidItem:
            return jsonify(invalidItem), 400

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
        if reqjson['i_name'].replace(' ', '') == '' and reqjson['i_name'] != '':
            return jsonify('Enter Item Name'), 400
        if not self.category_list.__contains__(reqjson['i_category']) and reqjson['i_category'] != '':
            return ('Category not valid'), 400
        if not isinstance(reqjson['i_stock'], int) or reqjson['i_stock'] < 0:
            return jsonify('Enter valid stock'), 400
        if reqjson['i_stock'] > 999999999:
            return jsonify('Stock cannot be greater than 999,999,999'), 400
        if (not isinstance(reqjson['i_price'], float) and not isinstance(reqjson['i_price'], int)) or reqjson['i_price'] < 0:
            return jsonify('Enter valid price'), 400

        oldjson = self.getDictByID(id)
        if oldjson:
            i_name = oldjson['Item Name']
            i_category = oldjson['Category']
            i_stock = oldjson['Stock']
            i_price = oldjson['Price']
            if reqjson['i_category'] != '':
                i_category = reqjson['i_category']
            if reqjson['i_name'] != '' and reqjson['i_name'] != oldjson['Item Name']:
                i_name = reqjson['i_name']
                if self.checkInvalidItem(i_name, i_category):
                    return ("Item already exists: %s in category %s" %(reqjson['i_name'], reqjson['i_category'])), 404
            if reqjson['i_stock'] != '':
                i_stock = reqjson['i_stock']
            if reqjson['i_price'] != '':
                i_price = reqjson['i_price']


            daoRes = self.dao.updateItemByID(id, i_name, i_category, i_stock, i_price)
            if daoRes:
                return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID %d not found' %id), 404

    def checkInvalidItem(self, i_name, i_category):
        if not self.category_list.__contains__(i_category):
            return 1
        invalidItem = self.dao.checkInvalidItem(i_name,i_category)
        if invalidItem:
            return 2
        return 0;

    def getLeastExpensiveItem(self):
        daoRes = self.dao.getAllAscendingPrice()
        cheapestPrice = -1
        if daoRes:
            res = []
            for row in daoRes:
                rowPrice = row[4]
                rowPrice = float(rowPrice.replace('$', '').replace(',', '')) # remove dollar sign and comma
                if rowPrice > cheapestPrice != -1: #break loop after finding first item above cheapest price
                    break
                cheapestPrice = rowPrice #first item in list sets cheapest price
                res.append(self.dictionary(row)) #add to list
            return jsonify(res), 200
        else:
            return jsonify('Item Table Empty! ...or error ocurred'), 400

    def getMostExpensiveItem(self):
        daoRes = self.dao.getAllDescendingPrice()
        cheapestPrice = -1
        if daoRes:
            res = []
            for row in daoRes:
                rowPrice = row[4]
                rowPrice = float(rowPrice.replace('$', '').replace(',', '')) # remove dollar sign and comma
                if rowPrice < cheapestPrice:  # break loop after finding first item below max price
                    break
                cheapestPrice = rowPrice  # first item in list sets max price
                res.append(self.dictionary(row))  # add to list
            return jsonify(res), 200
        else:
            return jsonify('Item Table Empty! ...or error ocurred'), 400

