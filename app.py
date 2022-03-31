from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

from controller.ItemController import ItemController
from controller.ItemsInCartController import ItemsInCartController
from controller.ItemsInOrderController import ItemsInOrderController
from controller.LikesController import LikesController
from controller.UserController import UserController
from controller.OrderController import OrderController

app = Flask(__name__)
CORS(app)

@app.route('/')
def empty():
    return 'Hello world'

#-----------------USERS---------------------------------
@app.route('/rumzon/users/all')
def allUsers():
    return UserController().getAll()

@app.route('/rumzon/users/<int:id>')
def userByID(id):
    return UserController().getByID(id)

@app.route('/rumzon/users/new', methods=['POST'])
def newUser():
    return UserController().addNewUser(request.json)

#-----------------ITEMS---------------------------------
@app.route('/rumzon/items/all')
def allItems():
    return ItemController().getAll()

@app.route('/rumzon/items/<int:id>', methods=['GET','DELETE','PUT'])
def itemByID(id):
    if request.method == 'GET':
        return ItemController().getByID(id)
    elif request.method == 'DELETE':
        return ItemController().deleteItem(id)
    elif request.method == 'PUT':
        return ItemController().updateItem(id, request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/items/new', methods=['POST'])
def newItem():
    return ItemController().addNewItem(request.json)

#-----------------ORDERS---------------------------------
@app.route('/rumzon/orders/all')
def allOrders():
    return OrderController().getAll()

@app.route('/rumzon/orders/<int:id>')
def orderByID(id):
    return OrderController().getByID(id)

#-----------------Likes---------------------------------
@app.route('/rumzon/likes/all')
def allLikes():
    return LikesController().getAll()

@app.route('/rumzon/likes/users/<int:id>')
def UserLikesByUserID(id):
    return LikesController().getUserLikesByUserID(id)

@app.route('/rumzon/likes/items/<int:id>')
def ItemLikesByItemID(id):
    return LikesController().getItemLikesByItemID(id)

#-----------------ItemsInCart---------------------------------
@app.route('/rumzon/itemsincart/all')
def allItemsInCarts():
    return ItemsInCartController().getAll()

@app.route('/rumzon/itemsincart/<int:id>',methods=['GET','DELETE'])
def cartItemsByUserID(id):
    if request.method == 'GET':
        return ItemsInCartController().getUserCartbyID(id)
    elif request.method == 'DELETE':
        return ItemsInCartController().clearUserCartbyID(id)
    else:
        return 'Request not handled'

#-----------------ItemsInOrder---------------------------------
@app.route('/rumzon/itemsinorder/all')
def allItemsInOrders():
    return ItemsInOrderController().getAll()

@app.route('/rumzon/itemsinorder/<int:id>')
def OrderItemsbyOrderID(id):
    return ItemsInOrderController().getOrderItemsbyID(id)


if __name__ == '__main__':
    app.run(debug=1)