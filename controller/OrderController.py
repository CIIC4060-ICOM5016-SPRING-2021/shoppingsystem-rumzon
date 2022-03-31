from flask import jsonify
from dao.OrderDAO import OrderDAO

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
            return jsonify(result)
        else:
            return jsonify('Order Table Empty!... or error ocurred'), 405

    def getByID(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405

    def getAllByUserID(self, uid):
        daoRes = self.dao.getByUserID(uid)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('ID Not Found'), 405

    def deleteOrder(self, id):
        daoRes = self.dao.getByID(id)
        if daoRes:
            self.dao.deleteOrder(id)
            return jsonify(self.dictionary(daoRes[0]))
        else:
            return jsonify('ID Not Found'), 405

    def updateOrder(self, id, json):
        daoRes = self.dao.getByID(id)
        o_time = json['o_time']
        u_id = json['u_id']
        if daoRes:
            self.dao.updateOrder(id, o_time, u_id)
            return jsonify(json), 201
        else:
            return jsonify('ID Not Found'), 405

    def addNewOrder(self, json):
        o_time = json['o_time']
        u_id = json['u_id']

        o_id = self.dao.addNewOrder(o_time, u_id)
        json['o_id'] = o_id
        return jsonify(json), 201
