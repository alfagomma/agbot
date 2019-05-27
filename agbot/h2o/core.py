
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
H2o SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.4"
__date__ = "2019-05-22"

import json
import logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

class H2o(object):
    """
    H2o core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init H2o')
        session = Session()
        self.apibot = session.apibot
        self.ep_h2o = session.ep_h2o

    #order
    def createOrder(self, payload):
        """
        Create new order
        """
        logger.debug('Creating order %s' % payload)
        rq = f'{self.ep_h2o}/order'
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        logger.info('Order %s created' % order['data']['id'])
        return order

    def getOrder(self, order_id:int):
        """
        Get order by id
        """
        logger.debug('Creating order %s' % payload)
        rq = f'{self.ep_h2o}/order/{order_id}'
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        return order        

    def getOrderFromErp(self, order_id, erp_id):
        """
        Read order from erp external ID.
        """
        logger.debug(f'Reading order {order_id} for erp {erp_id}')
        rq = f'{self.ep_h2o}/order/findByErpId'
        payload = {
            'erp_id': erp_id, 
            'ext_id': order_id 
            }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        logger.debug('Find order %s' % order['data']['id'])
        return order

    #customer
    def createCustomer(self, payload):
        """
        Create new customer.
        """
        logger.debug('Init creating customer...')
        print(payload)
        rq = f'{self.ep_h2o}/customer'
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logger.info('Customer %s created' % customer['data']['id'])
        return customer

    def getCustomer(self, customer_id:int):
        """
        Get customer by id.
        """
        logger.debug(f'Reading customer {customer_id}...')        
        rq = f'{self.ep_h2o}/customer/{customer_id}'
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        return customer

    def getCustomerFromErp(self, customer_id, erp_id):
        """
        Read customer from erp external ID
        """
        logger.debug(f'Reading customer {customer_id} for erp {erp_id}')
        rq = f'{self.ep_h2o}/customer/findByErpId'
        payload = {
            'erp_id': erp_id, 
            'ext_id': customer_id 
            }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logger.debug('Find customer %s' % customer['data']['id'])
        return customer
    
    def getCustomerFromVatcode(self, vatcode):
        """
        Read customer from vat code.
        """
        logger.debug(f'Reading customer from vat code {vatcode}')
        rq = f'{self.ep_h2o}/customer/findByVatcode'
        payload = {
            'vatcode': vatcode
            }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logger.debug('Find customer %s' % customer['data']['id'])
        return customer

    def getCustomerFromTaxcode(self, taxcode):
        """
        Read customer from tax code.
        """
        logger.debug(f'Reading customer from tax code {taxcode}')
        rq = f'{self.ep_h2o}/customer/findByTaxcode'
        payload = {
            'taxcode': taxcode
            }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logger.debug('Find customer %s' % customer['data']['id'])
        return customer

    def updateCustomer(self, customer_id, payload):
        """
        Update customer data.
        """
        logger.debug(f'Updating customer {customer_id}...')
        rq = f'{self.ep_h2o}/customer/{customer_id}'
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logger.debug(f'Updated customer {customer_id}')
        return customer

    def createCustomerXerp(self, customer_id:int, payload):
        """
        Update customer ERP Xrefs.
        """
        logger.debug(f'Init creating customer {customer_id} ERP xref ...')
        rq = f'{self.ep_h2o}/customer/{customer_id}/xerp'
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False

    def updateCustomerAddress(self, customer_id, payload):
        """
        Update customer address.
        """
        logger.debug(f'Init updating {customer_id} address ...')
        rq = f'{self.ep_h2o}/customer/{customer_id}/address'
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
    
    #competitor
    def createCompetitor(self, payload):
        """
        Create new competitor.
        """
        logger.debug('Init creating competitor...')
        rq = f'{self.ep_h2o}/competitor'
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        competitor = json.loads(r.text)
        logger.info('Competitor %s created' % competitor['data']['id'])

    def getCompetitor(self, competitor_id:int):
        """
        Get competitor by id.
        """
        logger.debug(f'Reading competitor {competitor_id}...')        
        rq = f'{self.ep_h2o}/competitor/{competitor_id}'
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        competitor = json.loads(r.text)
        return competitor    
    
    #currency

    #sales channel