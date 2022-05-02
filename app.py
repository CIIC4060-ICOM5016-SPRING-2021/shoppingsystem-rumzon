from flask import Flask, request
from flask_cors import CORS

from back_end.controller.ItemController import ItemController
from back_end.controller.ItemsInCartController import ItemsInCartController
from back_end.controller.ItemsInOrderController import ItemsInOrderController
from back_end.controller.LikesController import LikesController
from back_end.controller.UserController import UserController
from back_end.controller.OrderController import OrderController

app = Flask(__name__)
CORS(app)

@app.route('/')
def empty():
    return 'Hello world'

#-----------------USERS---------------------------------
@app.route('/rumzon/users/all')
def allUsers():
    return UserController().getAll()

@app.route('/rumzon/users', methods=['GET', 'DELETE', 'PUT'])
def userByID():
    if request.method == 'GET':
        return UserController().getByID(request.json)
    elif request.method == 'DELETE':
        return UserController().deleteUser(request.json)
    elif request.method == 'PUT':
        return UserController().updateUser(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/users/new', methods=['POST'])
def newUser():
    return UserController().addNewUser(request.json)

@app.route('/rumzon/users/login', methods=['POST'])
def login():
    return UserController().login(request.json)

#-----------------ITEMS---------------------------------
@app.route('/rumzon/items/all')
def allItems():
    return ItemController().getAll()

@app.route('/rumzon/items', methods=['GET','DELETE','PUT', 'POST'])
def itemFunctions():
    if request.method == 'GET':
        return ItemController().getByID(request.json)
    elif request.method == 'DELETE':
        return ItemController().deleteItem(request.json)
    elif request.method == 'PUT':
        return ItemController().updateItem(request.json)
    elif request.method == 'POST':
        return ItemController().addNewItem(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/items/category/<string:category_name>')
def filterItemsByCategory(category_name):
    return ItemController().getItemsFilterCategory(category_name)

@app.route('/rumzon/items/sort', methods =['POST'])
def organizeItems():
    if request.method == 'POST':
        return ItemController().getItemsSorted(request.json)
    else:
        return 'Request not handled'

#-----------------ORDERS---------------------------------
@app.route('/rumzon/orders/all')
def allOrders():
    return OrderController().getAll()

@app.route('/rumzon/orders/user')
def orderByUserID():
    return OrderController().getAllByUserID(request.json)

@app.route('/rumzon/orders', methods=['GET','DELETE'])
def orderByID():
    if request.method == 'GET':
        return OrderController().getByID(request.json['o_id'])
    elif request.method == 'DELETE':
        return OrderController().deleteOrder(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/orders/new', methods=['POST'])
def newOrder():
    return OrderController().addNewOrder(request.json)

#-----------------Likes---------------------------------
@app.route('/rumzon/likes', methods=['POST','DELETE'])
def userLikes():
    if request.method == 'POST':
        return LikesController().addLike(request.json)
    elif request.method == 'DELETE':
        return LikesController().deleteLike(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/likes/all')
def allLikes():
    return LikesController().getAll()

@app.route('/rumzon/likes/users')
def userLikesByUserID():
    return LikesController().getUserLikesByUserID(request.json)

@app.route('/rumzon/likes/items')
def itemLikesByItemID():
    return LikesController().getItemLikesByItemID(request.json)

#-----------------ItemsInCart---------------------------------
@app.route('/rumzon/cart/all')
def allItemsInCarts():
    return ItemsInCartController().getAll()

@app.route('/rumzon/cart', methods=['GET','DELETE','PUT','POST'])
def cartItemsByUserID():
    if request.method == 'GET':
        return ItemsInCartController().getUserCartByID(request.json)
    elif request.method == 'DELETE':
        return ItemsInCartController().deleteItemInCart(request.json)
    if request.method == 'POST':
        return ItemsInCartController().addToCart(request.json)
    if request.method == 'PUT':
        return ItemsInCartController().updateFromCart(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/cart/clear', methods=['DELETE'])
def clearCart():
    if request.method == 'DELETE':
        return ItemsInCartController().clearUserCartByID(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/cart/total')
def getUserCartTotal():
    return ItemsInCartController().getUserCartTotalByID(request.json)

@app.route('/rumzon/cart/buy', methods=['POST'])
def buyAllItemsInCarts():
    if request.method == 'POST':
        return ItemsInCartController().buyAllFromCart(request.json)
    else:
        return 'Request not handled'

#-----------------ItemsInOrder---------------------------------
@app.route('/rumzon/itemsinorder/all')
def allItemsInOrders():
    return ItemsInOrderController().getAll()

@app.route('/rumzon/itemsinorder')
def orderItemsbyOrderID():
    return ItemsInOrderController().getOrderItemsByOrderID(request.json)

#-----------------Global Statistics---------------------------------
@app.route('/rumzon/global/price/max')
def getMostExpensiveItem():
    return ItemController().getMostExpensiveItem()

@app.route('/rumzon/global/price/min')
def getLeastExpensiveItem():
    return ItemController().getLeastExpensiveItem()

@app.route('/rumzon/global/hot/items')
def getMostBoughtItems():
    return ItemsInOrderController().getMostBoughtItems(request.json["onlyActive"])

@app.route('/rumzon/global/hot/category')
def getMostBoughtCategory():
    return ItemsInOrderController().getMostBoughtCategories(request.json["onlyActive"])

@app.route('/rumzon/global/likes')
def mostLikes():
    return LikesController().getMostLikedItems()

#-----------------User Statistics---------------------------------

@app.route('/rumzon/users/<int:u_id>/hot/items')
def getUserMostBoughtItems(u_id):
    return ItemsInOrderController().getUserMostBoughtItems(u_id, request.json["onlyActive"])

@app.route('/rumzon/users/<int:u_id>/hot/category')
def getUserMostBoughtCategory(u_id):
    return ItemsInOrderController().getUserMostBoughtCategories(u_id, request.json["onlyActive"])

@app.route('/rumzon/users/<int:u_id>/itemsinorder/max')
def getUserMostExpensiveItemPurchase(u_id):
    return ItemsInOrderController().getUserMostExpensiveItemPurchase(u_id)

@app.route('/rumzon/users/<int:u_id>/itemsinorder/min')
def getUserLeastExpensiveItemPurchase(u_id):
    return ItemsInOrderController().getUserLeastExpensiveItemPurchase(u_id)

@app.route('/rumzon/users/<int:u_id>/orders/max')
def getUserMostExpensiveOrder(u_id):
    return OrderController().getUserMostExpensiveOrder(u_id)

@app.route('/rumzon/users/<int:u_id>/orders/min')
def getUserLeastExpensiveOrder(u_id):
    return OrderController().getUserLeastExpensiveOrder(u_id)

if __name__ == '__main__':
    app.run(debug=True)