from flask import Flask, render_template, request, Response
#from prometheus_client import Counter, generate_latest
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

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
    return render_template("main.html")

# metrics.register_default(
#     metrics.counter(
#         'by_path_counter', 'Request count by request paths',
#         labels={'path': lambda: request.path}
#     )
# )

if __name__ == "__main__":
    app.run()
