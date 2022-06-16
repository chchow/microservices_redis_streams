import atexit
import json

import requests

from common.utils import log_info, log_error
from lib.event_store import EventStore

store = EventStore()

def check_wallet(item):
    try:
        msg_data = json.loads(item['entity'])

# Cheers""".format(customer['name'], len(products), ", ".join([product['name'] for product in products]))

#         requests.post('http://msg-service:5000/email', json={
#             "to": customer['email'],
#             "msg": msg
#         })
        msg = """Checking wallet for {}!
        Adding total value for {} products from Smart Audio Sdn Bhd:
        {}
        """.format(msg_data['customer_id'], len(msg_data['product_ids']), ",".join(msg_data['product_ids']))
        
        log_info(msg)

        wallet_status = {
            'order_id': msg_data['order_id'],
            'customer_id': msg_data['customer_id'],
            'balance': 'ok'
        }
        store.publish('account', 'wallet', **wallet_status)
    except Exception as e:
        log_error(e)


def subscribe_to_domain_events():
    store.subscribe('inventory', 'check', check_wallet)
    log_info('subscribed to domain events')


def unsubscribe_from_domain_events():
    store.unsubscribe('inventory', 'check', check_wallet)
    log_info('unsubscribed from domain events')


subscribe_to_domain_events()
atexit.register(unsubscribe_from_domain_events)
