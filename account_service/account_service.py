import atexit
import json
import os

import requests

from common.utils import log_info, log_error
from lib.event_store import EventStore

store = EventStore()

def check_wallet(item):
    try:
        msg_data = json.loads(item['entity'])

        insufficient_fund = False
        if msg_data['inventory'] == 'payment-required':
            msg = """Checking wallet for {}! To be paid: {}
            """.format(msg_data['customer_id'], msg_data['order_total'])
            log_info(msg)

            account = store.find_one('account', msg_data['customer_id'])
            if int(account['balance']) >= int(msg_data['order_total']):
                account['balance'] = int(account['balance']) - int(msg_data['order_total'])
                store.publish('account', 'updated', **account)
            else:
                insufficient_fund = True
            if insufficient_fund:
                account_status = {
                    'order_id': msg_data['order_id'],
                    'customer_id': msg_data['customer_id'],
                    'account': 'insufficient-fund'
                }
            else:
                account_status = {
                    'order_id': msg_data['order_id'],
                    'customer_id': msg_data['customer_id'],
                    'account': 'to-be-shipped'
                }

            store.publish('account', 'wallet', **account_status)
        else:
            msg = """Account: nothing to proceess for order id {}, inventory status: {}
            """.format(msg_data['order_id'], msg_data['inventory'])
            log_info(msg)

    except Exception as e:
        log_error(e)


def subscribe_to_domain_events():
    store.subscribe('inventory', 'check', check_wallet)
    log_info('subscribed to domain events')


def unsubscribe_from_domain_events():
    store.unsubscribe('inventory', 'check', check_wallet)
    log_info('unsubscribed from domain events')


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    store.activate_entity_cache('account')
    atexit.register(store.deactivate_entity_cache, 'account')

subscribe_to_domain_events()
atexit.register(unsubscribe_from_domain_events)
