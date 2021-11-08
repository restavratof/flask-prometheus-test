import time
import random
import os

from flask import Flask
from flask import request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Gauge

# Create my app
app = Flask(__name__)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


# --- METRICS ----------------------------------------
# static information as metric
# metrics.info('app_info', 'Application info', version='0.1.0')
# # Dynamic metric
load_metric = Gauge('app_load', 'Application load to be used for HPA')


# Fibonacci function
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@app.route('/health')
def health():
    print(f'health - START')
    return 'OK'


@app.route('/fibonacci', methods=['POST'])
def fibonacci_route():
    print(f'fibonacci - IN')
    num = request.get_json().get('number')
    result = fibonacci(num)
    print(f'fibonacci - OUT: {result}')
    return f'RESULT: {result}'


@app.route('/load', methods=['POST'])
def load_route():
    print(f'load_route - IN')
    val = request.get_json().get('value')
    load_metric.set(val)
    print(f'load_route - OUT: {val}')
    return f'SET'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
