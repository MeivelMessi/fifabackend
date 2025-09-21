import json
from flask import Flask, request, jsonify
import os
from pyexpat.errors import messages
from pymongo import MongoClient
from bson import ObjectId
from jsonschema import validate, ValidationError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 🔹 MongoDB Connection
client = MongoClient("mongodb+srv://Meivel:Meivel2805@cluster0.j47yofn.mongodb.net/")
db = client["fifaDataBase"]
collection = db["fifaCollection"]

def check_schema(data):
    try:
        fifa_schema = {
        "type": "object",
        "properties": {
                "date": {"type": "string"},
                "ziva_score": {"type": "integer" },
                "anirudh_score": {"type": "integer"},
                "winner":{"type": "string"},
                "week": {"type": "integer"},
                "matchNumber": {"type": "integer"}
        },
        "required": ["date", "ziva_score", "anirudh_score", "winner"],  # ✅ required fields
         "additionalProperties": False  # ✅ block unknown keys
        }
        validate(instance=data, schema = fifa_schema)
        return True
    except ValidationError as e:
        return jsonify({"error": e.message}), 400


@app.route('/fifaCreate', methods=["POST"])
def create():
    data = request.get_json(silent=True)
    valid = check_schema(data)
    if valid is not True:
        return valid
    collection.insert_one(data)
    return jsonify({"message": "Created successfully"}), 201

@app.route('/fifa', methods=["GET"])
def get_fifa_data():
    params = request.args.get("q")
    if params:
        try:
            query =  json.loads(params)
            if query['_id']:
                query['_id'] = ObjectId(query['_id'])
        except json.JSONDecodeError:
             return jsonify({"message": 'jsonError'}),400
    else:
        query = {}
    result = list(collection.find(query))
    for res in result:
        res['_id'] = str(res['_id'])
    print('result', result)
    return  jsonify(result)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
