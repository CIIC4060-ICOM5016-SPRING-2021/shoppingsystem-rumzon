from controller import ListController
from flask import Flask
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


@app.route('/')
def ey():
    return 'test empty'

@app.route('/a')
def a():
    return 'test a'

@app.route('/list')
def list():
    return ListController.getList()

if __name__ == '__main__':
    app.run(debug=1)