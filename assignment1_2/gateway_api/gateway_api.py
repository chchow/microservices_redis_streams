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

def create_account():
    """
    Create an amount of test customers.

    :return: The generated customers.
    """
    customers = [
        { "id": "101", "name": "Anthony", "email": "anthony@server.com", "balance": 1000 },
        { "id": "102", "name": "Becky", "email": "Becky@server.com", "balance": 100 },
        { "id": "103", "name": "Carol", "email": "Carol@server.com", "balance": 1000 }
    ]
    return customers


def create_inventory():
    """
    Create an amount of test inventories.

    :return: The generated inventory.
    """
    
    inventory = [
        { "id": "201", "name": "Denon Speakers", "price": 800, "amount": 4 },
        { "id": "202", "name": "Sonos Speakers", "price": 600, "amount": 7 },
        { "id": "203", "name": "AudioPro Speakers", "price": 400, "amount": 4 },
        { "id": "204", "name": "Google Home Mini", "price": 100, "amount": 3 },
        { "id": "204", "name": "Xiaomi Soundbar", "price": 300, "amount": 8 }
    ]
    return inventory


@app.route('/order', methods=['POST'])
def order_command(order_id=None):

    return proxy_command_request('http://order-service:5000{}')

@app.route('/init-data', methods=['POST'])
def init_data():
    account_list = create_account()
    inventory_list = create_inventory()
    for account in account_list:
        store.publish('account', 'created', **account)
    for inventory in inventory_list:
        store.publish('inventory', 'created', **inventory)
    return json.dumps({"result": "success"})

@app.route('/report', methods=['GET'])
def report():

    result = {
        "accounts": store.find_all('account'),
        "inventory": store.find_all('inventory'),
        "orders": store.find_all('order'),
    }

    return json.dumps(result)
