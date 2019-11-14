
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
H2o SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.4"
__date__ = "2019-05-22"

import json, logging
from agbot.session import Session, parseApiError

logger = logging.getLogger()

class H2o(object):
    """
    H2o core class .
    """

    def __init__(self, profile_name='default'):
        """
        Initialize main class.
        """
        logger.debug('Init H2o SDK')
        session = Session(profile_name)
        self.agent = session.create()
        self.host = f'{session.getAgapiHost()}/h2o'

    #order
    def createOrder(self, payload):
        """
        Create new order
        """
        logger.debug('Creating order %s' % payload)
        rq = f'{self.host}/order'
        r = self.agent.post(rq, json=payload)
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
        logger.debug(f'Reading order {order_id}..')
        rq = f'{self.host}/order/{order_id}'
        r = self.agent.get(rq)
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
        rq = f'{self.host}/order/findByErpId'
        payload = {
            'erp_id': erp_id, 
            'ext_id': order_id 
            }
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        logger.debug('Find order %s' % order['data']['id'])
        return order

    #customer
    def getCustomers(self, query=None):
        """
        Read all customers.
        """
        logger.debug('Getting all customers')
        rq = '%s/customer' % (self.host)
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        _items = json.loads(r.text)
        return _items

    def createCustomer(self, payload):
        """
        Create new customer.
        """
        logger.debug('Init creating customer...')
        print(payload)
        rq = f'{self.host}/customer'
        r = self.agent.post(rq, json=payload)
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
        rq = f'{self.host}/customer/{customer_id}'
        r = self.agent.get(rq)
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
        rq = f'{self.host}/customer/findByErpId'
        payload = {
            'erp_id': erp_id, 
            'ext_id': customer_id 
            }
        r = self.agent.get(rq, params=payload)
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
        rq = f'{self.host}/customer/findByVatcode'
        payload = {
            'vatcode': vatcode
            }
        r = self.agent.get(rq, params=payload)
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
        rq = f'{self.host}/customer/findByTaxcode'
        payload = {
            'taxcode': taxcode
            }
        r = self.agent.get(rq, params=payload)
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
        rq = f'{self.host}/customer/{customer_id}'
        r = self.agent.post(rq, json=payload)
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
        rq = f'{self.host}/customer/{customer_id}/xerp'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False

    def updateCustomerAddress(self, customer_id, payload):
        """
        Update customer address.
        """
        logger.debug(f'Init updating {customer_id} address ...')
        rq = f'{self.host}/customer/{customer_id}/address'
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
    
    #competitor
    def createCompetitor(self, payload):
        """
        Create new competitor.
        """
        logger.debug('Init creating competitor...')
        rq = f'{self.host}/competitor'
        r = self.agent.post(rq, json=payload)
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
        rq = f'{self.host}/competitor/{competitor_id}'
        r = self.agent.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        competitor = json.loads(r.text)
        return competitor    
    
    #currency

    #sales channel