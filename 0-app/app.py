import time
import random
import os

from flask import Flask
from flask import request
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app, export_defaults=False)

# --- METRICS ----------------------------------------
# static information as metric
metrics.info('app_info', 'Application info', version='0.1.0')
# Dynamic metric
load_metric = metrics.info('app_load', 'Application load to be used for HPA')
# Fib
req_counter = metrics.counter(
    'http_requests_total',
    'Total number of http requests',
    labels={'method': lambda: request.method}
)


# Fibonacci function
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@app.route('/health')
@req_counter
def health():
    print(f'health - START')
    return 'OK'


@app.route('/fibonacci', methods=['POST'])
@req_counter
def fibonacci_route():
    print(f'fibonacci - IN')
    num = request.get_json().get('number')
    result = fibonacci(num)
    print(f'fibonacci - OUT: {result}')
    return f'RESULT: {result}'


@app.route('/load', methods=['POST'])
@req_counter
def load_route():
    print(f'load_route - IN')
    val = request.get_json().get('value')
    load_metric.set(val)
    print(f'load_route - OUT: {val}')
    return f'SET'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
