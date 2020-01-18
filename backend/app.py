from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/shows", methods=['GET'])
def get_all_shows():
    return create_response({"shows": db.get('shows')})

@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if not id.isdigit(): #type safety
        return create_response(status=404, message="No show with this id exists")
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")

@app.route("/shows/<id>", methods=['GET'])
def get_show(id):
    if not id.isdigit():
        return create_response(status=404, message="No show with this id exists")
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    return create_response(result= db.getById('shows', int(id)))

@app.route("/shows", methods=['POST'])
def make_show():
    # could have just used request.args, felt safer checking if we're actually getting JSON
    if request.json is None:
        return create_response(status=422, message="The request is not in proper JSON format.")
    if 'name' not in request.json:
        return create_response(status=422, message="There is no name provided.")
    if 'episodes_seen' not in request.json:
        return create_response(status=422, message="There is no episode count provided.")
    if len(request.json)>2:
        return create_response(status=422, message="The request is too long.")

    body = {
        'name':request.json['name'],
        'episodes_seen':request.json['episodes_seen'],
        'id':0
    }
    result = db.create('shows', body)
    return create_response({"result": db.getById('shows',int(result["id"]))}, status=201)

@app.route("/shows/<id>",methods=["PUT"])
def update_show(id):
    if request.json is None:
        return create_response(status=422, message="The request is not in proper JSON format.")
    if len(request.json)>2:
        return create_response(status=422, message="The request is too long.")
    if not id.isdigit(): 
        return create_response(status=404, message="No show with this id exists")
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")

    change = dict()
    if 'name' in request.json:
        change.update({'name':request.json['name']})
    if 'episodes_seen' in request.json:
        change.update({'episodes_seen':request.json['episodes_seen']})
    db.updateById('shows',int(id),change)
    return create_response({"result": db.getById('shows', int(id))}, status=201)





# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
