from flask import jsonify
import json

from controller.UserController import UserController
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
        if not self.category_list.__contains__(i_category):
            return jsonify("Category '%s' does not exist" % i_category), 400
        daoRes = self.dao.getItemsFilterCategory(i_category)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Category Empty! ... or error occured'), 404

    def getItemsSorted(self, json):
        if json['sortBy'].lower() != 'price' and json['sortBy'].lower() != 'name':
            return jsonify("'Sort By' must be 'price' or 'name'"), 400
        if json['sortType'].lower() != 'descending' and json['sortType'].lower() != 'ascending':
            return jsonify("'Sort Type' must be 'ascending' or 'descending'"), 400

        daoRes = []
        if json['sortBy'].lower() == 'price' and json['sortType'].lower() == 'ascending':
            daoRes = self.dao.getAllAscendingPrice()
        elif json['sortBy'].lower() == 'price' and json['sortType'].lower() == 'descending':
            daoRes = self.dao.getAllDescendingPrice()
        elif json['sortBy'].lower() == 'name' and json['sortType'].lower() == 'ascending':
            daoRes = self.dao.getAllAscendingName()
        elif json['sortBy'].lower() == 'name' and json['sortType'].lower() == 'descending':
            daoRes = self.dao.getAllDescendingName()

        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Item Table Empty!... or error occurred'), 405

    def getByID(self, json):
        daoRes = self.isActive(json['item_id'])
        if daoRes == 1:
            return jsonify(self.dictionary(self.dao.getByID(json['item_id'])[0])), 200
        # elif daoRes == 0:
        #     return jsonify('Item %s is inactive' %json['item_id']), 404
        else:
            return jsonify('ID Not Found'), 404


    def getDictByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return self.dictionary(daoRes[0])
        else:
            return 0

    def isActive(self, item_id):
        daoRes = self.dao.isActive(item_id)
        if daoRes:
            for row in daoRes:
                if row[0] == True:
                    return 1 #item is active
                else:
                    return 0 #item is inactive
        else:
            return -1 #item id not found or error

    def addNewItem(self, json):
        if not isinstance(json['u_id'], int):
            return jsonify("Enter valid User ID integer"), 400

        isAdmin = UserController().isAdmin(json['u_id'])
        if isAdmin == 0:
            return jsonify('User %d does not have admin privileges' % json['u_id']), 403
        elif isAdmin == -1:
            return jsonify('User %d not found' % json['u_id']), 404

        if json['i_name'].replace(' ', '') == '':
            return jsonify('Enter Item Name'), 400
        if json['i_category'] == '':
            return jsonify('Enter Category'), 400
        if not isinstance(json['i_stock'], int) or json['i_stock'] <= 0:
            return jsonify('Stock must be Integer greater than 0'), 400
        if json['i_stock'] > 999999999:
            return jsonify('Stock cannot be greater than 999,999,999'), 400
        if not isinstance(json['i_price'], float) and not isinstance(json['i_price'], int):
            return jsonify('Price must be Integer or Float'), 400
        if json['i_price'] < 0:
            return jsonify('Enter Valid Price'), 400

        invalidItem = self.checkInvalidItem(json['i_name'], json['i_category'])
        if invalidItem == 1:
            return jsonify("Category '%s' does not exist" %json['i_category']), 400

        inactiveID = self.dao.inactiveID(json['i_name'], json['i_category'])
        if inactiveID:
            i_stock = json['i_stock']
            i_price = json['i_price']
            daoRes = self.dao.reactivateItem(inactiveID[0][0], i_price, i_stock)
            if daoRes:
                res = []
                res.append("Item reactivated")
                res.append(self.dictionary(daoRes[0]))
                return jsonify(res)
            else:
                return jsonify('Error reactivating item: %s, %s' %(json['i_name'], json['i_category'])), 500
        if invalidItem == 2:
            return jsonify("Item '%s' already exists in category '%s'" %(json['i_name'], json['i_category'])), 400

        i_name = json['i_name']
        i_category = json['i_category']
        i_stock = json['i_stock']
        i_price = json['i_price']
        daoRes = self.dao.addNewItem(i_name, i_category, i_stock, i_price)
        if daoRes:
            return self.dictionary(daoRes[0])
        else:
            return jsonify('Error creating item'), 500

    def deleteItem(self, json):
        if not isinstance(json['u_id'], int):
            return jsonify("Enter valid User ID integer"), 400
        if not isinstance(json['item_id'], int):
            return jsonify("Enter valid Item ID integer"), 400

        isAdmin = UserController().isAdmin(json['u_id'])
        if isAdmin == 0:
            return jsonify('User %d does not have admin privileges' % json['u_id']), 403
        elif isAdmin == -1:
            return jsonify('User ID %d not found' % json['u_id']), 404

        isActive = self.isActive(json['item_id'])
        if isActive == 1:
            daoRes = self.dao.getByID(json['item_id'])
            self.dao.deleteItemByID(json['item_id'])
            return jsonify(self.dictionary(daoRes[0]))
        # elif isActive == 0:
        #     return jsonify('Item %d is inactive' % json['item_id']), 404
        else:
            return jsonify('Item ID %d Not Found' % json['item_id']), 404

    def updateItem(self, reqjson):
        if not isinstance(reqjson['u_id'], int):
            return jsonify("Enter valid User ID integer"), 400
        isAdmin = UserController().isAdmin(reqjson['u_id'])
        if isAdmin == 0:
            return jsonify('User %d does not have admin privileges' % reqjson['u_id']), 403
        elif isAdmin == -1:
            return jsonify('User %d not found' % reqjson['u_id']), 404

        isActive = self.isActive(reqjson['item_id'])
        if isActive == 1:
            oldjson = self.getDictByID(reqjson['item_id'])
            #verify new values
            if reqjson['i_name'].replace(' ', '') == '' and reqjson['i_name'] != '':
                return jsonify('Enter Item Name'), 400
            if not self.category_list.__contains__(reqjson['i_category']) and reqjson['i_category'] != '':
                return jsonify('Category "%s" does not exist' % reqjson['i_category']), 400
            if reqjson['i_stock'] != '':
                if not isinstance(reqjson['i_stock'], int) or reqjson['i_stock'] < 0:
                    return jsonify('Stock must be integer greater than 0'), 400
                if reqjson['i_stock'] > 999999999:
                    return jsonify('Stock cannot be greater than 999,999,999'), 400
            if reqjson['i_price'] != '' and \
                    ((not isinstance(reqjson['i_price'], float) and not isinstance(reqjson['i_price'], int)) or \
                    reqjson['i_price'] < 0):
                return jsonify('Price must be valid float or integer '), 400


            #get old values
            i_name = oldjson['Item Name']
            i_category = oldjson['Category']
            i_stock = oldjson['Stock']
            i_price = oldjson['Price']

            #change old values with new values
            if reqjson['i_category'] != '':
                i_category = reqjson['i_category']
            if reqjson['i_name'] != '' and reqjson['i_name'] != oldjson['Item Name']:
                i_name = reqjson['i_name']
                if self.checkInvalidItem(i_name, i_category):
                    return jsonify("Item '%s' already exists in category '%s'" % (i_name, i_category)), 400
            if reqjson['i_stock'] != '':
                i_stock = reqjson['i_stock']
            if reqjson['i_price'] != '':
                i_price = reqjson['i_price']

            daoRes = self.dao.updateItemByID(reqjson['item_id'], i_name, i_category, i_stock, i_price)
            if daoRes:
                return jsonify(self.dictionary(daoRes[0])), 200
        # elif isActive == 0:
        #     return jsonify('Item %d is inactive' % reqjson['item_id']), 404
        else:
            return jsonify('ID %d not found' % reqjson['item_id']), 404


    def checkInvalidItem(self, i_name, i_category):
        if not self.category_list.__contains__(i_category):
            return 1 # category does not exist
        invalidItem = self.dao.checkInvalidItem(i_name,i_category)
        if invalidItem:
            return 2 # name and category combo already exist
        return 0 # item valid

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

