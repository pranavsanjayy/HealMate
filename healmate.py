from flask import Flask, request, jsonify
import uuid
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

fileName = "pills.json"


# API to add pill schedule
@app.route('/healMate/input', methods=['POST'])
def post_input():

    pill = request.form.get('pill')
    time = request.form.get('time')

    data = {
        "pill": pill,
        "time": time,
        "id": str(uuid.uuid4())
    }

    # Load existing data safely
    if os.path.exists(fileName):
        with open(fileName, "r") as f:
            try:
                jsondata = json.load(f)
            except:
                jsondata = []
    else:
        jsondata = []

    jsondata.append(data)

    with open(fileName, "w") as f:
        json.dump(jsondata, f, indent=4)

    return jsonify({
        "message": "data added",
        "pill": pill,
        "time": time
    })


# API to fetch pill schedules
@app.route('/healMate/fetch', methods=['GET'])
def get_data():

    if os.path.exists(fileName):
        with open(fileName, "r") as f:
            try:
                jsondata = json.load(f)
            except:
                jsondata = []

        return jsonify(jsondata)

    return jsonify({"message": "no data present"})


# API to delete pill schedule
@app.route('/healMate/delete/<id>', methods=['DELETE'])
def delete_data(id):

    if not os.path.exists(fileName):
        return jsonify({"message": "no data present"})

    with open(fileName, "r") as f:
        try:
            jsondata = json.load(f)
        except:
            jsondata = []

    newdata = [item for item in jsondata if item["id"] != id]

    with open(fileName, "w") as f:
        json.dump(newdata, f, indent=4)

    return jsonify({
        "message": "data deleted",
        "id": id
    })


# Run server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)