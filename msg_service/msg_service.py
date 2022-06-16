import atexit
import json

import requests

from common.utils import log_info, log_error
from lib.event_store import EventStore

store = EventStore()

def customer_created(item):
    try:
        msg_data = json.loads(item['entity'])
        msg = """Dear {}!

Welcome to Ordershop.

Cheers""".format(msg_data['name'])

        requests.post('http://msg-service:5000/email', json={
            "to": msg_data['email'],
            "msg": msg
        })
    except Exception as e:
        log_error(e)


def customer_deleted(item):
    try:
        msg_data = json.loads(item['entity'])
        msg = """Dear {}!

Good bye, hope to see you soon again at Ordershop.

Cheers""".format(msg_data['name'])

        requests.post('http://msg-service:5000/email', json={
            "to": msg_data['email'],
            "msg": msg
        })
    except Exception as e:
        log_error(e)


def order_created(item):
    try:
        msg_data = json.loads(item['entity'])

# Cheers""".format(customer['name'], len(products), ", ".join([product['name'] for product in products]))

#         requests.post('http://msg-service:5000/email', json={
#             "to": customer['email'],
#             "msg": msg
#         })
        msg = """Dear {}!
        Thank you for buying following {} products from Smart Audio Sdn Bhd:
        {}

        Cheers""".format(msg_data['customer_id'], len(msg_data['product_ids']), ",".join(msg_data['product_ids']))
        
        log_info(msg)
    except Exception as e:
        log_error(e)


def subscribe_to_domain_events():
    store.subscribe('order', 'created', order_created)
    log_info('subscribed to domain events')


def unsubscribe_from_domain_events():
    store.unsubscribe('order', 'created', order_created)
    log_info('unsubscribed from domain events')


subscribe_to_domain_events()
atexit.register(unsubscribe_from_domain_events)
