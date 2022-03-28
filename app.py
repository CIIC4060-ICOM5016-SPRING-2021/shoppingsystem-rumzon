from controller import ListController
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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