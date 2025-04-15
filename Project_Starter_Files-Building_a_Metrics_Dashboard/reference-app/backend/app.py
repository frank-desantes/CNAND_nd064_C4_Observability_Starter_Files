from flask import Flask, render_template, request, jsonify

import pymongo
from flask_pymongo import PyMongo
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

CORS(app)  # Set CORS for development

mongo = PyMongo(app)

# Track HTTP status codes
metrics.counter(
    'http_status_codes',
    'Count of HTTP status codes',
    labels={'status': lambda r: r.status_code}
)

@app.after_request
def track_errors(response):
    if 400 <= response.status_code < 600:
        # Increment custom metric for errors
        metrics.counter(
            'http_error_codes',
            'Count of HTTP error codes',
            labels={'status': response.status_code}
        )
    return response

@app.route("/")
def homepage():
    return "Hello World"


@app.route("/api")
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    star = mongo.db.stars
    name = request.json["name"]
    distance = request.json["distance"]
    star_id = star.insert({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run()
