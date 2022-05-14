from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from subprocess import Popen


def qu4nt_launcher(settings_object_id):
    qu4nt_root_path = "/home/simone/Scrivania/trading/codice_nuovo/ok/Qu4ntProcessor/"
    command = "python3 {}main.py --settings_id {}".format(qu4nt_root_path, settings_object_id)
    proc = Popen(command, shell=True,
                 stdin=None, stdout=None, stderr=None, close_fds=True)
    return proc.pid


@app.route('/run_qu4nt', methods=['POST'])
def run_qu4nt():
    if request.method == 'POST':
        created_setting = mongo.db.qu4nt_settings.insert_one(request.json)
        process_id = qu4nt_launcher(str(created_setting.inserted_id))
        mongo.db.qu4nt_settings.update_one({'_id': created_setting.inserted_id}, {'$set': {"process_id": process_id}})
        result = {
            "settings_object_id": str(created_setting.inserted_id),
            "process_id": process_id,
        }
        resp = jsonify(result)
        resp.status_code = 201
        return resp
    else:
        return not_found()


@app.route('/get_settings/<settings_object_id>')
def get_settings(settings_object_id):
    if ObjectId.is_valid(settings_object_id):
        result = mongo.db.qu4nt_settings.find_one({'_id': ObjectId(settings_object_id)})
        return check_result(result)
    else:
        return jsonify({})


@app.route('/get_settings')
def get_setting():
    result = mongo.db.qu4nt_settings.find()
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
    app.run(port=8081)
