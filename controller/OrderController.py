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