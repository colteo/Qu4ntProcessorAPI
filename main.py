from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request


@app.route('/qu4nt_inputs', methods=['POST'])
def add_inputs():
    if request.method == 'POST':
        _json = request.json
        result = mongo.db.qu4nt_inputs.insert_one(_json)
        object_id = dict({"id": str(result.inserted_id)})
        resp = jsonify(object_id)
        resp.status_code = 201
        return resp
    else:
        return not_found()


@app.route('/qu4nt_inputs/<object_id>')
def get_input_detail(object_id):
    if ObjectId.is_valid(object_id):
        result = mongo.db.qu4nt_inputs.find_one({'_id': ObjectId(object_id)})
        return check_result(result)
    else:
        return jsonify({})


@app.route('/qu4nt_inputs')
def get_inputs():
    result = mongo.db.qu4nt_inputs.find()
    return check_result(result)


def check_result(result):
    if result is not None:
        resp = dumps(result)
    else:
        resp = jsonify({})
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()
