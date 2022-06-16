import atexit
import json

import requests

from common.utils import log_info, log_error
from lib.event_store import EventStore

store = EventStore()

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
        We are currently processing your order.
        Cheers""".format(msg_data['customer_id'], len(msg_data['product_ids']), ",".join(msg_data['product_ids']))
        
        log_info(msg)
    except Exception as e:
        log_error(e)

def account_notify(item):
    try:
        msg_data = json.loads(item['entity'])

# Cheers""".format(customer['name'], len(products), ", ".join([product['name'] for product in products]))

#         requests.post('http://msg-service:5000/email', json={
#             "to": customer['email'],
#             "msg": msg
#         })
        msg = """Dear {}!
        Order ID: {} is on the way to you.

        Cheers""".format(msg_data['customer_id'], msg_data['order_id'])
        
        log_info(msg)
    except Exception as e:
        log_error(e)


def subscribe_to_domain_events():
    store.subscribe('order', 'created', order_created)
    store.subscribe('account', 'wallet', account_notify)
    log_info('subscribed to domain events')


def unsubscribe_from_domain_events():
    store.unsubscribe('order', 'created', order_created)
    store.unsubscribe('account', 'wallet', account_notify)
    log_info('unsubscribed from domain events')


subscribe_to_domain_events()
atexit.register(unsubscribe_from_domain_events)
