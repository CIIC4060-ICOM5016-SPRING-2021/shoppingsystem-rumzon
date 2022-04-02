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

@app.route('/rumzon/users/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def userByID(id):
    if request.method == 'GET':
        return UserController().getByID(id)
    elif request.method == 'DELETE':
        return UserController().deleteUser(id)
    elif request.method == 'PUT':
        return UserController().updateUser(id, request.json)
    else:
        return 'Request not handled'

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

@app.route('/rumzon/items/category/<string:category_name>')
def filterItemsByCategory(category_name):
    return ItemController().getItemsFilterCategory(category_name)

@app.route('/rumzon/items/price/asc')
def allAscendingPrice():
    return ItemController().getAllAscendingPrice()

@app.route('/rumzon/items/price/desc')
def allDescendingPrice():
    return ItemController().getAllDescendingPrice()

@app.route('/rumzon/items/name/asc')
def AllAscendingName():
    return ItemController().getAllAscendingName()

@app.route('/rumzon/items/name/desc')
def allDescendingName():
    return ItemController().getAllDescendingName()

#-----------------ORDERS---------------------------------
@app.route('/rumzon/orders/all')
def allOrders():
    return OrderController().getAll()

@app.route('/rumzon/orders/user/<int:id>')
def orderByUserID(id):
    return OrderController().getAllByUserID(id)

@app.route('/rumzon/orders/<int:id>', methods=['GET','DELETE','PUT'])
def orderByID(id):
    if request.method == 'GET':
        return OrderController().getByID(id)
    elif request.method == 'DELETE':
        return OrderController().deleteOrder(id)
    elif request.method == 'PUT':
        return OrderController().updateOrder(id, request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/orders/new', methods=['POST'])
def newOrder():
    return OrderController().addNewOrder(request.json)

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

@app.route('/rumzon/itemsincart/<int:id>', methods=['GET','DELETE'])
def cartItemsByUserID(id):
    if request.method == 'GET':
        return ItemsInCartController().getUserCartByID(id)
    elif request.method == 'DELETE':
        return ItemsInCartController().clearUserCartByID(id)
    else:
        return 'Request not handled'

@app.route('/rumzon/itemsincart/<int:id>/total')
def getUserCartTotal(id):
    return ItemsInCartController().getUserCartTotalByID(id)

@app.route('/rumzon/itemsincart/buyall/<int:id>', methods=['GET', 'POST'])
def buyAllItemsInCarts(id):
    return ItemsInCartController().buyAllFromCart(id)

#-----------------ItemsInOrder---------------------------------
@app.route('/rumzon/itemsinorder/all')
def allItemsInOrders():
    return ItemsInOrderController().getAll()

@app.route('/rumzon/itemsinorder/<int:id>')
def OrderItemsbyOrderID(id):
    return ItemsInOrderController().getOrderItemsByID(id)


if __name__ == '__main__':
    app.run(debug=1)