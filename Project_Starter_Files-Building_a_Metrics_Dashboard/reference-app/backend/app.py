from flask import Flask, render_template, request, jsonify

import pymongo
from flask_pymongo import PyMongo
from flask_opentracing import FlaskTracing

from flask_cors import CORS

from prometheus_flask_exporter import PrometheusMetrics

from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

import logging
logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
metrics = PrometheusMetrics(app)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"
mongo = PyMongo(app)

CORS(app)  # Set CORS for development

def init_tracer(service):
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            "reporter_batch_size": 1,
            'logging': True,
        },
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
        service_name=service,
        validate=True,
    )
    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('backend')
flask_tracer = FlaskTracing(tracer, True, app)


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
    with tracer.start_span('BackendSpan') as span:
        answer = "something"
        span.set_tag("api", answer)        
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
