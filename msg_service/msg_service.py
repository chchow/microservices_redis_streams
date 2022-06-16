import atexit
import json

import requests

from common.utils import log_info, log_error
from lib.event_store import EventStore

store = EventStore()

def order_created(item):
    try:
        msg_data = json.loads(item['entity'])

        msg = """Dear {}!
        Thank you for buying following {} products from Smart Audio Sdn Bhd:
        {}
        We are currently processing your order.
        Cheers""".format(msg_data['customer_id'], len(msg_data['product_ids']), ",".join(msg_data['product_ids']))
        
        log_info(msg)
    except Exception as e:
        log_error(e)

def inventory_notify(item):
    try:
        msg_data = json.loads(item['entity'])

        account = store.find_one('account', msg_data['customer_id'])
        if msg_data['inventory'] == 'out-of-stock':
            msg = """Dear {},
            We're sorry that some of your order items are out of stock at the moment for Order ID: {}.
            The order is now on back to back order. Bear with us and we will keep you notified.

            Cheers""".format(account['name'], msg_data['order_id'])
            
            log_info(msg)
        else:
            msg = """Dear {},
            All items in Order ID: {} are in stock.
            Will proceed for process payment.

            Cheers""".format(account['name'], msg_data['order_id'])
            
            log_info(msg)
 
    except Exception as e:
        log_error(e)

def account_notify(item):
    try:
        msg_data = json.loads(item['entity'])

        account = store.find_one('account', msg_data['customer_id'])
        if msg_data['account'] == 'to-be-shipped':
            msg = """Dear {},
            Order ID: {} is on the way to you.

            Cheers""".format(account['name'], msg_data['order_id'])
            
            log_info(msg)
        else:
            msg = """Dear {},
            Order ID: {} requires your attention due to insufficient fund.
            Do top up your wallet and process payment.

            Cheers""".format(account['name'], msg_data['order_id'])
            
            log_info(msg)
 
    except Exception as e:
        log_error(e)


def subscribe_to_domain_events():
    store.subscribe('order', 'created', order_created)
    store.subscribe('inventory', 'check', inventory_notify)
    store.subscribe('account', 'wallet', account_notify)
    log_info('subscribed to domain events')


def unsubscribe_from_domain_events():
    store.unsubscribe('order', 'created', order_created)
    store.unsubscribe('inventory', 'check', inventory_notify)
    store.unsubscribe('account', 'wallet', account_notify)
    log_info('unsubscribed from domain events')


subscribe_to_domain_events()
atexit.register(unsubscribe_from_domain_events)
