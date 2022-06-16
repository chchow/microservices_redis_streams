import atexit
import json
import os

import requests

from common.utils import log_info, log_error
from lib.event_store import EventStore

store = EventStore()

def check_inventory(item):
    try:
        msg_data = json.loads(item['entity'])

        msg = """Checking inventory for order {} with product_ids: {}
        """.format(msg_data['id'], ",".join(msg_data['product_ids']))
        log_info(msg)

        occurs = {}
        out_of_stock = False
        total_price = 0
        try:
            product_ids = msg_data['product_ids']
        except KeyError:
            raise ValueError("missing mandatory parameter 'product_ids'")

        for inventory in store.find_all('inventory'):

            if not inventory['id'] in occurs:
                occurs[inventory['id']] = 0

            occurs[inventory['id']] += product_ids.count(inventory['id'])
            if occurs[inventory['id']] <= int(inventory['amount']):
                continue
            else:
                msg = """Insufficient {} stock for order {}
                """.format(inventory['name'], msg_data['id'])
                log_info(msg)

                out_of_stock = True
                

        for k, v in occurs.items():
            inventory = list(filter(lambda x: x['id'] == k, store.find_all('inventory')))
            if not inventory:
                raise ValueError("could not find inventory")

            inventory = inventory[0]
            if int(inventory['amount']) - v >= 0:

                inventory['amount'] = int(inventory['amount']) - v
                total_price += int(inventory['price']) * v

                msg = """Reserving {} stock for order {}
                """.format(inventory['name'], msg_data['id'])
                log_info(msg)
                # trigger event
                store.publish('inventory', 'updated', **inventory)

            else:
                msg = """Error while decrementing {} stock for order {}
                """.format(inventory['name'], msg_data['id'])
                log_info(msg)

                out_of_stock = True
        if out_of_stock:
            inventory_status = {
                'inventory': 'out-of-stock',
                'order_id': msg_data['id'],
                'customer_id': msg_data['customer_id'],
                'product_ids': msg_data['product_ids']
            }
        else:
            inventory_status = {
                'inventory': 'payment-required',
                'order_id': msg_data['id'],
                'customer_id': msg_data['customer_id'],
                'product_ids': msg_data['product_ids'],
                'order_total' : total_price
            }
        store.publish('inventory', 'check', **inventory_status)
    except Exception as e:
        log_error(e)


def subscribe_to_domain_events():
    store.subscribe('order', 'created', check_inventory)
    log_info('subscribed to domain events')


def unsubscribe_from_domain_events():
    store.unsubscribe('order', 'created', check_inventory)
    log_info('unsubscribed from domain events')


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    store.activate_entity_cache('inventory')
    atexit.register(store.deactivate_entity_cache, 'inventory')

subscribe_to_domain_events()
atexit.register(unsubscribe_from_domain_events)
