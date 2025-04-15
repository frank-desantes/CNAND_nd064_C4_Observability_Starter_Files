from flask import Flask, render_template, request, Response
#from prometheus_client import Counter, generate_latest
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

# Define a Prometheus counter to track HTTP status codes
#HTTP_STATUS_CODES = Counter('http_status_codes', 'HTTP status codes returned by the Flask app', ['status_code'])

# @app.after_request
# def track_status_code(response):
#     # Increment the counter for the status code of the response
#     #print("Increment the counter for the status code of the response")
#     HTTP_STATUS_CODES.labels(status_code=response.status_code).inc()
#     return response

# @app.route('/metrics')
# def metrics():
#     # Expose metrics for Prometheus
#     #print("Expose metrics for Prometheus")
#     return Response(generate_latest(), mimetype='text/plain')

@app.route("/")
def homepage():
    return render_template("main.html")

# metrics.register_default(
#     metrics.counter(
#         'by_path_counter', 'Request count by request paths',
#         labels={'path': lambda: request.path}
#     )
# )

if __name__ == "__main__":
    app.run()
