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

@app.route('/rumzon/users', methods=['POST', 'DELETE', 'PUT'])
def userByID():
    if request.method == 'POST':
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

@app.route('/rumzon/items', methods=['DELETE','PUT', 'POST'])
def itemFunctions():
    if request.method == 'POST':
        return ItemController().getByID(request.json)
    elif request.method == 'DELETE':
        return ItemController().deleteItem(request.json)
    elif request.method == 'PUT':
        return ItemController().updateItem(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/items/new', methods=['POST'])
def newItem():
    return ItemController().addNewItem(request.json)

@app.route('/rumzon/items/category/<string:category_name>')
def filterItemsByCategory(category_name):
    return ItemController().getItemsFilterCategory(category_name)

@app.route('/rumzon/items/sort', methods =['POST'])
def organizeItems():
    return ItemController().getItemsSorted(request.json)

#-----------------ORDERS---------------------------------
@app.route('/rumzon/orders/all')
def allOrders():
    return OrderController().getAll()

@app.route('/rumzon/orders/user', methods =['POST'])
def orderByUserID():
    if request.method == 'POST':
        return OrderController().getAllByUserID(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/orders', methods=['POST','DELETE'])
def orderByID():
    if request.method == 'POST':
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

@app.route('/rumzon/likes/users', methods=['POST'])
def userLikesByUserID():
    return LikesController().getUserLikesByUserID(request.json)

@app.route('/rumzon/likes/items', methods=['POST'])
def itemLikesByItemID():
    return LikesController().getItemLikesByItemID(request.json)

#-----------------ItemsInCart---------------------------------
@app.route('/rumzon/cart/all')
def allItemsInCarts():
    return ItemsInCartController().getAll()

@app.route('/rumzon/cart', methods=['DELETE','PUT','POST'])
def cartItemsByUserID():
    if request.method == 'POST':
        return ItemsInCartController().getUserCartByID(request.json)
    elif request.method == 'DELETE':
        return ItemsInCartController().deleteItemInCart(request.json)
    if request.method == 'PUT':
        return ItemsInCartController().updateFromCart(request.json)
    else:
        return 'Request not handled'

@app.route('/rumzon/cart/add', methods=['POST'])
def addItemToUserCart():
    return ItemsInCartController().addToCart(request.json)

@app.route('/rumzon/cart/clear', methods=['DELETE'])
def clearCart():
    return ItemsInCartController().clearUserCartByID(request.json)

@app.route('/rumzon/cart/total', methods=['POST'])
def getUserCartTotal():
    return ItemsInCartController().getUserCartTotalByID(request.json)

@app.route('/rumzon/cart/buy', methods=['POST'])
def buyAllItemsInCarts():
    return ItemsInCartController().buyAllFromCart(request.json)


#-----------------ItemsInOrder---------------------------------
@app.route('/rumzon/itemsinorder/all')
def allItemsInOrders():
    return ItemsInOrderController().getAll()

@app.route('/rumzon/itemsinorder', methods=['POST'])
def orderItemsbyOrderID():
    return ItemsInOrderController().getOrderItemsByOrderID(request.json)

#-----------------Global Statistics---------------------------------
@app.route('/rumzon/global/price/max')
def getMostExpensiveItem():
    return ItemController().getMostExpensiveItem()

@app.route('/rumzon/global/price/min')
def getLeastExpensiveItem():
    return ItemController().getLeastExpensiveItem()

@app.route('/rumzon/global/hot/items', methods=['POST'])
def getMostBoughtItems():
    return ItemsInOrderController().getMostBoughtItems(request.json["onlyActive"])

@app.route('/rumzon/global/hot/category', methods=['POST'])
def getMostBoughtCategory():
    return ItemsInOrderController().getMostBoughtCategories(request.json["onlyActive"])

@app.route('/rumzon/global/likes')
def mostLikes():
    return LikesController().getMostLikedItems()

#-----------------User Statistics---------------------------------

@app.route('/rumzon/users/hot/items', methods=['POST'])
def getUserMostBoughtItems():
    return ItemsInOrderController().getUserMostBoughtItems(request.json["u_id"], request.json["onlyActive"])

@app.route('/rumzon/users/hot/category', methods=['POST'])
def getUserMostBoughtCategory():
    return ItemsInOrderController().getUserMostBoughtCategories(request.json["u_id"], request.json["onlyActive"])

@app.route('/rumzon/users/itemsinorder/max', methods=['POST'])
def getUserMostExpensiveItemPurchase():
    return ItemsInOrderController().getUserMostExpensiveItemPurchase(request.json["u_id"])

@app.route('/rumzon/users/itemsinorder/min', methods=['POST'])
def getUserLeastExpensiveItemPurchase():
    return ItemsInOrderController().getUserLeastExpensiveItemPurchase(request.json["u_id"])

@app.route('/rumzon/users/orders/max', methods=['POST'])
def getUserMostExpensiveOrder():
    return OrderController().getUserMostExpensiveOrder(request.json["u_id"])

@app.route('/rumzon/users/orders/min', methods=['POST'])
def getUserLeastExpensiveOrder():
    return OrderController().getUserLeastExpensiveOrder(request.json["u_id"])

if __name__ == '__main__':
    app.run(debug=True)