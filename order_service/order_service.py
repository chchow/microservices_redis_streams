import json
import uuid

import requests

from flask import request
from flask import Flask

from common.utils import check_rsp_code
from lib.event_store import EventStore


app = Flask(__name__)
store = EventStore()


def create_order(_product_ids, _customer_id):
    """
    Create an order entity.

    :param _product_ids: The product IDs the order is for.
    :param _customer_id: The customer ID the order is made by.
    :return: A dict with the entity properties.
    """
    return {
        'id': str(uuid.uuid4()),
        'product_ids': _product_ids,
        'customer_id': _customer_id,
        'status': 'pending'
    }

@app.route('/order', methods=['POST'])
def post():
    value = request.get_json()
    new_order = {}
    try:
        new_order = create_order(value['product_ids'],value['customer_id'])
    except KeyError:
        raise ValueError("missing mandatory paramter 'product_ids' and/or 'customer_id")

    app.logger.info("order to be publish")
    store.publish('order', 'created', **new_order)
    return json.dumps(new_order)