from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

from controller.ItemController import ItemController
from controller.UserController import UserController
from controller.OrderController import OrderController

app = Flask(__name__)
CORS(app)

@app.route('/')
def empty():
    return 'Hello world'

#-----------------USERS---------------------------------
@app.route('/rumzon/Users/all')
def allUsers():
    return UserController().getAll()

@app.route('/rumzon/Users/<int:id>')
def userByID(id):
    return UserController().getByID(id)

#-----------------ITEMS---------------------------------
@app.route('/rumzon/Items/all')
def allItems():
    return ItemController().getAll()

@app.route('/rumzon/Items/<int:id>')
def itemByID(id):
    return ItemController().getByID(id)

#-----------------ORDERS---------------------------------
@app.route('/rumzon/Orders/all')
def allOrders():
    return OrderController().getAll()

@app.route('/rumzon/Orders/<int:id>')
def orderByID(id):
    return OrderController().getByID(id)

@app.route('/rumzon/Likes/all')
def all_likes():
    cursor.execute('SELECT * FROM likes')
    res = cursor.fetchall()
    return jsonify(res)

@app.route('/rumzon/ItemsInOrder/all')
def all_items_in_order():
    cursor.execute('SELECT *, itemTotal(item_id, o_ammount) AS i_total FROM itemsinorder')
    res = cursor.fetchall()
    return jsonify(res)

@app.route('/rumzon/ItemsInCart/all')
def all_items_in_cart():
    cursor.execute('SELECT *, itemTotal(item_id, c_ammount) AS i_total FROM itemsincart')
    res = cursor.fetchall()
    return jsonify(res)

@app.route('/rumzon/ItemsInCart/clear/<string:u_id>',methods = ['DELETE','GET'])
def clear_cart_for_user(u_id):
    if request.method == 'DELETE':
        cursor.execute('delete from itemsincart where u_id = ' + u_id)
        connection.commit()
        return "deleted"
    else:
        return 'el hehe'

if __name__ == '__main__':
    app.run(debug=1)