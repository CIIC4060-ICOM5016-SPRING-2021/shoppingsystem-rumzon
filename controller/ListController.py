from flask import jsonify


def getList():
    P1 = {'thing': 1, 'hehes':100, 'name':'Guy'}
    P2 = {'thing': 2, 'hehes': 1, 'name': 'Lad'}
    P3 = {'thing': 3, 'hehes': 10, 'name': 'Boy'}
    P4 = {'thing': 4, 'hehes': 50, 'name': 'Man'}

    return jsonify(P1, P2, P3, P4)