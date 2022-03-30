from controller import ListController
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Establish detabase connection
connection = psycopg2.connect(
    host='ec2-18-235-114-62.compute-1.amazonaws.com',
    database='de9v4rj4hthhg6',
    user='subtdkpfoxqmiu',
    password='660b482966304513c9478db7907c698d30fe3c81aa41efb9161884c7d6df7434')

# Open a cursor to perform database operations
cursor = connection.cursor()
connection.commit()


@app.route('/')
def empty():
    return 'Hello world'

@app.route('/rumzon/Users/all')
def all_users():
    cursor.execute('SELECT * FROM users')
    res = cursor.fetchall()
    return jsonify(res)

@app.route('/rumzon/Items/all')
def all_items():
    cursor.execute('SELECT * FROM items')
    res = cursor.fetchall()
    return jsonify(res)


@app.route('/rumzon/Orders/all')
def all_orders():
    cursor.execute('SELECT *, orderTotal(o_id) AS o_total FROM orders')
    res = cursor.fetchall()
    return jsonify(res)

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