from flask import jsonify
from dao.LikesDAO import LikesDAO
from dao.UserDAO import UserDAO
from dao.ItemDAO import ItemDAO
class LikesController:

    def __init__(self):
        self.dao = LikesDAO()

    def dictionary(self, row):
        dic = {}
        dic['Item ID'] = row[0]
        dic['User ID'] = row[1]
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

    def isValid(self, u_id, i_id):
        userIDValid = UserDAO().getByID(u_id)
        itemIDValid = ItemDAO().getByID(i_id)
        if userIDValid and itemIDValid:
            return True
        else:
            return False

    def addLike(self, u_id, i_id):

        if self.isValid(u_id, i_id):
            daoRes = self.dao.addLike(u_id, i_id)
            if not daoRes:
                return jsonify('Your like is already in the system'), 409
            return self.dictionary(daoRes[0]), 200
        else:
            return jsonify('User_ID or Item_ID Not Found'), 404

    def deleteLike(self, u_id, i_id):
        if self.isValid(u_id, i_id):
            daoRes = self.dao.deleteLike(u_id, i_id)
            if not daoRes:
                return jsonify('Your like has already been removed'), 409
            return self.dictionary(daoRes[0]), 200
        else:
            return jsonify('User_ID or Item_ID Not Found'), 404
