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

        if json['i_name'] == '':
            return jsonify('Enter Item Name'), 418
        if json['i_category'] == '':
            return jsonify('Enter Category'), 418
        if json['i_stock'] == '' or json['i_stock'] <= 0:
            return jsonify('Enter Valid Stock'), 418
        if json['i_price'] == '' or json['i_price'] < 0:
            return jsonify('Enter Valid Price'), 418

        invalidItem = self.checkValidItem(json['i_name'], json['i_category'])
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
                return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID %d not found' %id), 404

    def checkValidItem(self, i_name, i_category):
        if not self.category_list.__contains__(i_category):
            return ('Category not valid')
        invalidItem = self.dao.checkInvalidItem(i_name,i_category)
        if invalidItem:
            return ('Item already exists')
        return None;

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

    def getMostBoughtItems(self):
        daoRes = self.dao.getItemsPurchaseCount()
        maxCount = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[2] < maxCount: #break loop after finding first item below max purchases
                    break
                maxCount = row[2] #first item in list sets max purchases

                purchaseCountDic = {} #prepare return format
                purchaseCountDic['Item ID'] = row[0]
                purchaseCountDic['Name'] = row[1]
                purchaseCountDic['Purchase Count'] = row[2]
                res.append(purchaseCountDic) #add to list
            return jsonify(res), 200
        else:
            return jsonify('Like Table Empty! ...or error ocurred'), 400

    def getMostBoughtCategory(self):
        daoRes = self.dao.getCategoryPurchaseCount()
        maxCount = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[1] < maxCount: #break loop after finding first item below max purchases
                    break
                maxCount = row[1] #first item in list sets max purchases
                purchaseCountDic = {} #prepare return format
                purchaseCountDic['Category'] = row[0]
                purchaseCountDic['Purchase Count'] = row[1]
                res.append(purchaseCountDic) #add to list
            return jsonify(res), 200
        else:
            return jsonify('Like Table Empty! ...or error ocurred'), 400

    def getMostBoughtCategoryAll(self):
        daoRes = self.dao.getCategoryPurchaseCount()
        if daoRes:
            res = []
            for row in daoRes:
                purchaseCountDic = {} #prepare return format
                purchaseCountDic['Category'] = row[0]
                purchaseCountDic['Purchase Count'] = row[1]
                res.append(purchaseCountDic) #add to list
            return jsonify(res), 200
        else:
            return jsonify('Like Table Empty! ...or error ocurred'), 400