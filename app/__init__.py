import json
import uuid

from flask import Flask, request

app = Flask(__name__)

database = {
    'users': [],
    'properties': []
}


@app.route('/')
def show_index():
    return "Hello world!"


@app.route('/users', methods=['POST'])
def create_user():
    j = request.json
    record = {
        'id': str(uuid.uuid4()),
        'name': j['name']
    }
    database['users'].append(record)
    return json.dumps(record), 200


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    index = None

    for (ii, record) in enumerate(database['users']):
        if record['id'] == user_id:
            index = ii
            break

    if index is not None:
        del database['users'][index]
        return "", 200
    else:
        return json.dumps({'error': 'user id %s not found' % user_id}), 404


@app.route('/properties', methods=['POST'])
def create_property():
    j = request.json

    record = {
        'id': str(uuid.uuid4()),
        'owner': j['owner'],
        'desc': j['desc']
    }
    database['properties'].append(record)
    return json.dumps(record), 200


@app.route('/properties/<property_id>', methods=['DELETE'])
def delete_property(property_id):
    index = None

    for (ii, record) in enumerate(database['properties']):
        if record['id'] == property_id:
            index = ii
            break

    if index is not None:
        del database['properties'][index]
        return "", 200
    else:
        j = {'error': 'property id %s not found' % property_id}
        return json.dumps(j), 404


@app.route('/properties/<property_id>', methods=['GET'])
def get_property(property_id):
    index = None

    for (ii, record) in enumerate(database['properties']):
        if record['id'] == property_id:
            index = ii
            break

    if index is not None:
        return json.dumps(database['properties'][index]), 200
    else:
        j = {'error': 'property id %s not found' % property_id}
        return json.dumps(j), 404


@app.route('/properties/<property_id>', methods=['PUT'])
def update_property(property_id):
    j = request.json

    record = None

    for (ii, rr) in enumerate(database['properties']):
        if rr['id'] == property_id:
            record = rr
            break

    if record is not None:
        for k in j:
            record[k] = j[k]
        return json.dumps(record), 200
    else:
        j = {'error': 'property id %s not found' % property_id}
        return json.dumps(j), 404
