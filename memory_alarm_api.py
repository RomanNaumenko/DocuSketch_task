from datetime import date, datetime
from flask import Flask, request, jsonify
from mongo_utils import MongoDBConnection

app = Flask(__name__)


@app.route("/", methods=["GET", "POST", "PUT"])
def alarms():
    if request.method == "GET":
        with MongoDBConnection("admin", "admin", "localhost") as db:
            collection = db["alarm_status"]
            output = collection.find()
            return jsonify({'result': [[result["Date"], result["Time"], result["Point"], result["Status"]]
                                       for result in output]})

    if request.method == "POST":
        current_date = date.today().strftime("%m/%d/%y")
        current_time = datetime.now().strftime("%H:%M:%S")
        with MongoDBConnection("admin", "admin", "localhost") as db:
            collection = db["alarm_status"]
            object_id = collection.insert_one(
                {'Date': current_date, 'Time': current_time, 'Point': request.json["Point"],
                 'Status': request.json["Status"]}).inserted_id

        return jsonify({"id": f"{object_id}"})

    if request.method == "PUT":
        with MongoDBConnection("admin", "admin", "localhost") as db:
            collection = db["alarm_status"]
            collection.update_one({"_id": request.json["id"]},
                                  {"$set": {'Data': request.json["Data"], 'Time': request.json["Time"], 'Point': request.json["Point"], 'Status': request.json["Status"]}})
            return jsonify({"id": f'{request.json["id"]}'})


# 127.0.0.1

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
