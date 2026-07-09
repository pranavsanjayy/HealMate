from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
fileName="pills.json"

# Fake DB (dictionary for now, can later use SQLite/MySQL)
pill_schedule = {
    "user1": {
        "pill_name": "Paracetamol",
        "schedule": ["08:00", "12:00", "18:00"],
        "dose": 1
    }
}

dispense_logs = []

# API to get schedule
@app.route('/getSchedule/<user>', methods=['GET'])
def get_schedule(user):
    if user in pill_schedule:
        return jsonify(pill_schedule[user])
    else:
        return jsonify({"error": "User not found"}), 404

# API to log dispense data
@app.route('/logDispense', methods=['POST'])
def log_dispense():
    data = request.json
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dispense_logs.append(data)
    return jsonify({"message": "Log stored", "log": data})

# API to view logs
@app.route('/getLogs', methods=['GET'])
def get_logs():
    return jsonify(dispense_logs)




# API to post pill data
@app.route('/healMate/input', methods=['POST'])
def post_input():
    pill=request.form.get('pill')
    time=request.form.get('time')

    data={"pill":pill,"time":time}

    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        with open(fileName,"r") as f:
            jsondata=json.load(f)
        jsondata.append(data)

        with open(fileName,"w") as f:
            json.dump(jsondata,f,indent=4)
        return {"message": "data added", "pill": pill,"time": time}

    else:
        with open(fileName,"w") as f:
            json.dump([data],f,indent=4)
        return {"message": "data created", "pill": pill,"time": time}
    

#API to fetch
@app.route('/healMate/fetch', methods=['GET'])
def get_data():
    if os.path.exists(fileName) and os.path.getsize(fileName) > 0:
        with open(fileName,"r") as f:
            jsondata=json.load(f)
            return jsondata
    else:
        return {"message":"no data present"}


            

    
if __name__ == '__main__':
    app.run(debug=True)