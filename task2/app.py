import time
import datetime

import redis
from flask import Flask, request

import json

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_past_requests(current_data):
    retries = 5
    while True:
        try:
            cache.lpush('data', current_data)
            return cache.lrange('data', 0, -2)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
@app.route('/')
def hello():
    time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    ip = request.remote_addr
    info = get_past_requests("{} {}".format(time, ip))
    return 'Alexey Savenkov! Past requests:\n\n{}'.format('\n'.join(map(lambda x: x.decode("utf-8"), info))).replace('\n', '<br>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
