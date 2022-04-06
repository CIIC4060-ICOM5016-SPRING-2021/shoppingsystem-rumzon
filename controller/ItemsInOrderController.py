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
            return jsonify('No sales yet!... or error ocurred'), 405

    def getOrderItemsByOrderID(self, id):
        daoRes = self.dao.getOrderItemsByOrderID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("ID Not Found! ...or error ocurred" %id), 405

    def getMostBoughtItems(self):
        daoRes = self.dao.getItemsPurchaseCount()
        maxCount = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[2] < maxCount:  # break loop after finding first item below max purchases
                    break
                maxCount = row[2]  # first item in list sets max purchases

                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Item ID'] = row[0]
                purchaseCountDic['Name'] = row[1]
                purchaseCountDic['Purchase Count'] = row[2]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('No sales yet! ...or error ocurred'), 400

    def getMostBoughtCategory(self):
        daoRes = self.dao.getCategoryPurchaseCount()
        maxCount = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[1] < maxCount:  # break loop after finding first item below max purchases
                    break
                maxCount = row[1]  # first item in list sets max purchases
                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Category'] = row[0]
                purchaseCountDic['Purchase Count'] = row[1]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('No sales yet! ...or error ocurred'), 400

    def getCategoryPurchaseDesc(self):
        daoRes = self.dao.getCategoryPurchaseCount()
        if daoRes:
            res = []
            for row in daoRes:
                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Category'] = row[0]
                purchaseCountDic['Purchase Count'] = row[1]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('No sales yet! ...or error ocurred'), 400

    def getUserMostBoughtItems(self, u_id):
        daoRes = self.dao.getUserItemsPurchaseCount(u_id)
        maxCount = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[2] < maxCount:  # break loop after finding first item below max purchases
                    break
                maxCount = row[2]  # first item in list sets max purchases

                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Item ID'] = row[0]
                purchaseCountDic['Name'] = row[1]
                purchaseCountDic['Purchase Count'] = row[2]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('User #%s does not have purchases! ...or error ocurred' %u_id), 400

    def getUserMostBoughtCategory(self, u_id):
        daoRes = self.dao.getUserCategoryPurchaseCount(u_id)
        maxCount = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[1] < maxCount:  # break loop after finding first item below max purchases
                    break
                maxCount = row[1]  # first item in list sets max purchases
                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Category'] = row[0]
                purchaseCountDic['Purchase Count'] = row[1]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('User #%s does not have purchases! ...or error ocurred' %u_id), 400

    def getUserMostExpensiveItemPurchase(self, u_id):
        daoRes = self.dao.getUserMostExpensiveItemPurchase(u_id)
        if daoRes:
            res = []
            for row in daoRes:
                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Order ID'] = row[0]
                purchaseCountDic['Item ID'] = row[1]
                purchaseCountDic['Item Name'] = row[2]
                purchaseCountDic['Category'] = row[3]
                purchaseCountDic['Order Ammount'] = row[4]
                purchaseCountDic['Total'] = row[5]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('User #%s does not have purchases! ...or error ocurred' %u_id), 404

    def getUserLeastExpensiveItemPurchase(self, u_id):
        daoRes = self.dao.getUserLeastExpensiveItemPurchase(u_id)
        if daoRes:
            res = []
            for row in daoRes:
                purchaseCountDic = {}  # prepare return format
                purchaseCountDic['Order ID'] = row[0]
                purchaseCountDic['Item ID'] = row[1]
                purchaseCountDic['Item Name'] = row[2]
                purchaseCountDic['Category'] = row[3]
                purchaseCountDic['Order Ammount'] = row[4]
                purchaseCountDic['Total'] = row[5]
                res.append(purchaseCountDic)  # add to list
            return jsonify(res), 200
        else:
            return jsonify('User #%s does not have purchases! ...or error ocurred' %u_id), 404
