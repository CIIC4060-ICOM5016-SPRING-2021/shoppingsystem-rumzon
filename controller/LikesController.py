from flask import jsonify
from dao.LikesDAO import LikesDAO

class LikesController:

    def __init__(self):
        self.dao = LikesDAO()

    def dictionary(self, row):
        dic = {}
        dic['item_id'] = row[0]
        dic['u_id'] = row[1]
        return dic

    def getAll(self):
        daoRes = self.dao.getAll()
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify('Like Table Empty!... or error ocurred'), 405

    def getUserLikesByUserID(self, id):
        daoRes = self.dao.getUserLikesByUserID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("User #%d has no likes, or ID Not Found" %id), 405

    def getItemLikesByItemID(self, id):
        daoRes = self.dao.getItemLikesByItemID(id)
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("Item #%d has no likes, or ID Not Found" %id), 405