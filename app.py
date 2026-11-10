# Smart Parking Space Allocator
# Hemant Agrawal - 25293916039
# Anubhav - 25293916018

from flask import Flask, jsonify, render_template, request

import parking_lot

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/slots")
def slots():
    return jsonify(parking_lot.get_state())


@app.route("/allocate", methods=["POST"])
def allocate():
    data = request.get_json(silent=True) or {}
    result = parking_lot.allocate(
        data.get("number", ""),
        data.get("type", ""),
        data.get("priority", ""),
    )
    return jsonify(result)


@app.route("/release", methods=["POST"])
def release():
    data = request.get_json(silent=True) or {}
    result = parking_lot.release(data.get("number", ""))
    return jsonify(result)


@app.route("/find", methods=["POST"])
def find():
    data = request.get_json(silent=True) or {}
    result = parking_lot.find(data.get("number", ""))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
