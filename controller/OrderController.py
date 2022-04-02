from flask import jsonify
from dao.OrderDAO import OrderDAO
from dao.UserDAO import UserDAO
class OrderController:

    def __init__(self):
        self.dao = OrderDAO()

    def dictionary(self, row):
        dic = {}
        dic['u_id'] = row[0]
        dic['o_id'] = row[1]
        dic['o_time'] = row[2]
        dic['o_total'] = row[3]
        return dic

    def getAll(self):
        daoRes = self.dao.getAll()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result), 200
        else:
            return jsonify('Order Table Empty!... or error ocurred'), 400

    def getByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def getDictByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return self.dictionary(daoRes[0])
        else:
            return {}

    def getAllByUserID(self, uid):
        daoRes = self.dao.getByUserID(uid)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result), 200
        else:
            return jsonify('ID Not Found'), 404

    def deleteOrder(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteOrder(id)
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 405

    def updateOrder(self, o_id, reqjson):
        userIDValid = UserDAO().getByID(reqjson['u_id'])
        if not userIDValid:
            return jsonify('Invalid User ID'), 400

        oldjson = self.getDictByID(id)
        if oldjson:
            u_id = oldjson['u_id']
            if reqjson['u_id'] != '':
                u_id = reqjson['u_id']

            daoRes = self.dao.updateOrder(o_id, u_id)
            return jsonify(self.dictionary(daoRes[0])), 200
        else:
            return jsonify('ID Not Found'), 404

    def addNewOrder(self, reqjson):
        userIDValid = UserDAO().getByID(reqjson['u_id'])
        if not userIDValid:
            return jsonify('Invalid User ID'), 400

        u_id = reqjson['u_id']
        o_id = self.dao.addNewOrder(u_id)
        if o_id:
            reqjson['o_id'] = o_id
            return jsonify(reqjson), 200
        else:
            return jsonify('ID Not Found'), 404
