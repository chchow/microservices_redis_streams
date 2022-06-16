import json
import uuid

import requests

from flask import request
from flask import Flask

from common.utils import check_rsp_code
from lib.event_store import EventStore


app = Flask(__name__)
store = EventStore()


def proxy_command_request(_base_url):
    """
    Helper function to proxy POST, PUT and DELETE requests to the according service.

    :param _base_url: The URL of the service.
    """

    # handle POST
    if request.method == 'POST':

        try:
            values = json.loads(request.data)
        except Exception:
            raise ValueError("cannot parse json body {}".format(request.data))

        rsp = requests.post(_base_url.format(request.full_path), json=values)
        return check_rsp_code(rsp)

    # handle PUT
    if request.method == 'PUT':

        try:
            values = json.loads(request.data)
        except Exception:
            raise ValueError("cannot parse json body {}".format(request.data))

        rsp = requests.put(_base_url.format(request.full_path), json=values)
        return check_rsp_code(rsp)

    # handle DELETE
    if request.method == 'DELETE':
        rsp = requests.delete(_base_url.format(request.full_path))
        return check_rsp_code(rsp)

@app.route('/order', methods=['POST'])
def order_command(order_id=None):

    return proxy_command_request('http://order-service:5000{}')
