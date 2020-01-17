
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
    def __init__(self, profile_name=False):
        """
        Initialize main class.
        """
        logger.debug('Init H2o SDK')
        session = Session(profile_name)
        rqagent =  session.create()
        if not rqagent:
            logger.error('Unable to start h2o core without valid session.')
            exit(1)
        self.agent = rqagent
        self.host = f'{session.getAgapiHost()}/h2o'

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
        customer = json.loads(r.text)
        return customer

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
        rq = f'{self.host}/customer/findByErp'
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
    
    def getCustomerFromTax(self, code):
        """
        Read customer from tax code.
        """
        logger.debug(f'Reading customer from tax code {code}')
        rq = f'{self.host}/customer/findByTaX'
        payload = {
            'code': code
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
        resp = json.loads(r.text)
        return resp            

    #customer address
    def createCustomerAddress(self, customer_id:int, payload):
        """
        Create new customer address
        """
        logger.debug(f'Creating customer {customer_id} address')
        rq = f'{self.host}/customer/{customer_id}/address'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        address = json.loads(r.text)
        return address

    def updateCustomerAddress(self, customer_id:int, address_id:int, payload):
        """
        Update customer address.
        """
        logger.debug(f'Init updating {customer_id} address {address_id} ...')
        rq = f'{self.host}/customer/{customer_id}/address/{address_id}'
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        address = json.loads(r.text)
        return address
    
    def getCustomerAddresses(self, customer_id:int, query=None):
        """
        List customer addresses.
        """
        logger.debug(f'Getting all customer {customer_id} addresses')
        rq = '{self.host}/customer/{customer_id}/address'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        addresses = json.loads(r.text)
        return addresses

    def getCustomerAddress(self, customer_id:int, address_id:int, params=None):
        """
        Get customer address.
        """
        logger.debug(f'Get customer {customer_id} address {address_id}')
        rq = f'{self.host}/customer/{customer_id}/address/{address_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        address = json.loads(r.text)
        return address

    def getCustomerAddressFromExtId(self, customer_id:int, ext_id:str, query=None):
        """
        List customer addresses.
        """
        logger.debug(f'Search customer {customer_id} address ext_id {ext_id}.')
        payload ={
            'ext_id' : ext_id
        }
        if query:
            new_payload = dict(item.split("=") for item in query.split('&'))
            payload = {**payload, **new_payload}        
        rq = f'{self.host}/customer/{customer_id}/address/findByExtId'
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        address= json.loads(r.text)
        return address
        
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
        return competitor

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
    
    #order
    def createOrder(self, payload):
        """
        Create new order.
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

    def getOrders(self, query=None):
        """
        Read all orders.
        """
        logger.debug('Getting orders.')
        rq = f'{self.host}/order'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        orders = json.loads(r.text)
        return orders

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

    def getOrderFromErp(self, erp_id:int, ext_id):
        """
        Read order from erp external ID.
        """
        logger.debug(f'Reading order {ext_id} for erp {erp_id}')
        rq = f'{self.host}/order/findByErp'
        payload = {
            'erp_id': erp_id, 
            'ext_id': ext_id 
            }
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        logger.debug('Find order %s' % order['data']['id'])
        return order

    #order type
    def getOrderTypes(self, query=None):
        """
        Read all order types.
        """
        logger.debug('Getting order types.')
        rq = f'{self.host}/order/type'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        orderTypes = json.loads(r.text)
        return orderTypes

    def getOrderTypeFromName(self, name:str):
        """
        Get order type by name.
        """
        logger.debug('Getting order types.')
        rq = f'{self.host}/order/type/findByName'
        payload={
            'name':name
        }
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            return False
        orderType = json.loads(r.text)
        return orderType        

    def createOrderType(self, payload):
        """
        Create new order type.
        """
        logger.debug('Creating new order type.')
        rq = f'{self.host}/order/type'
        r = self.agent.get(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        orderType = json.loads(r.text)
        logger.info(f"Order type {orderType['data']['id']} created")
        return orderType        