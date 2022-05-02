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
            return jsonify('Like Table Empty! ...or error ocurred'), 405

    def getUserLikesByUserID(self, json):
        daoRes = self.dao.getUserLikesByUserID(json["u_id"])
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("User #%d has no likes, or ID Not Found" %json["u_id"]), 405

    def getItemLikesByItemID(self, json):
        daoRes = self.dao.getItemLikesByItemID(json['item_id'])
        if daoRes:
            result = []
            for row in daoRes:
                result.append(self.dictionary(row))
            return jsonify(result)
        else:
            return jsonify("Item #%d has no likes, or ID Not Found" %json['item_id']), 405

    def isValid(self, u_id, i_id):
        userIDValid = UserDAO().getByID(u_id)
        itemIDValid = ItemDAO().getByID(i_id)
        if not userIDValid:
            return 1
        if not itemIDValid:
            return 2
        return 0

    def addLike(self, json):
        isValid = self.isValid(json['u_id'], json['item_id'])
        if isValid == 1:
            return jsonify('User ID not found'), 404
        if isValid == 2:
            return jsonify('Item ID not found'), 404

        daoRes = self.dao.addLike(json['u_id'], json['item_id'])
        if not daoRes:
            return jsonify('User #%s already likes item #%s' %(json['u_id'], json['item_id'])), 409
        return self.dictionary(daoRes[0]), 200

    def deleteLike(self, json):
        isValid = self.isValid(json['u_id'], json['item_id'])
        if isValid == 1:
            return jsonify('User ID not found'), 404
        if isValid == 2:
            return jsonify('Item ID not found'), 404

        daoRes = self.dao.deleteLike(json['u_id'], json['item_id'])
        if not daoRes:
            return jsonify('User #%s does not like item #%s' %(json['u_id'],json['item_id'])), 409
        return self.dictionary(daoRes[0]), 200

    def getMostLikedItems(self):
        daoRes = self.dao.getLikeCount()
        maxLike = 0
        if daoRes:
            res = []
            for row in daoRes:
                if row[3] < maxLike: #break loop after finding first item below max likes
                    break
                maxLike = row[3] #first item in list sets max likes

                likeCountDic = {} #prepare return format
                likeCountDic['Item ID'] = row[0]
                likeCountDic['Name'] = row[1]
                likeCountDic['Category'] = row[2]
                likeCountDic['Like Count'] = row[3]
                res.append(likeCountDic) #add to list
            return jsonify(res), 200
        else:
            return jsonify('Like Table Empty! ...or error ocurred'), 400