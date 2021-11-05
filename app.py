import time
import random
import os

from flask import Flask
from flask import request
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='0.1.0')

common_counter = metrics.counter(
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


@app.route('/actuator/one')
@metrics.do_not_track()
def first_route():
    print(f'one')
    time.sleep(random.random() * 0.4)
    return 'one - ok'


@app.route('/fibonacci', methods=['GET'])
def the_second():
    print(f'two')


    return 'two - ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
