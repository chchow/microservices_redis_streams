import atexit
import json
import os
import uuid

import requests

from flask import request
from flask import Flask

from common.utils import check_rsp_code
from lib.event_store import EventStore
from common.utils import log_info, log_error


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
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    store.activate_entity_cache('order')
    atexit.register(store.deactivate_entity_cache, 'order')

@app.route('/order', methods=['POST'])
def post():
    value = request.get_json()
    new_order = {}
    try:
        new_order = create_order(value['product_ids'],value['customer_id'])
    except KeyError:
        raise ValueError("missing mandatory paramter 'product_ids' and/or 'customer_id")

    msg = """New order {} created: {}
    """.format(new_order['id'], ",".join(new_order['product_ids']))
    app.logger.info(msg)
    store.publish('order', 'created', **new_order)
    return json.dumps(new_order)

def update_order_status(item):
    msg_data = json.loads(item['entity'])
    order = store.find_one('order', msg_data['order_id'])
    if 'inventory' in msg_data:
        order['status'] = msg_data['inventory']
    if 'account' in msg_data:
        order['status'] = msg_data['account']
    else:
        order['status'] = 'unknown'
    msg = """Order {} status changed to {} with items: {}
    """.format(order['id'], order['status'], ",".join(order['product_ids']))
    app.logger.info(msg)
    store.publish('order', 'updated', **order)


def subscribe_to_domain_events():
    store.subscribe('inventory', 'check', update_order_status)
    store.subscribe('account', 'wallet', update_order_status)
    log_info('subscribed to domain events')

def unsubscribe_from_domain_events():
    store.unsubscribe('inventory', 'check', update_order_status)
    store.unsubscribe('account', 'wallet', update_order_status)
    log_info('unsubscribed from domain events')

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    store.activate_entity_cache('order')
    atexit.register(store.deactivate_entity_cache, 'order')
    subscribe_to_domain_events()
    atexit.register(unsubscribe_from_domain_events)