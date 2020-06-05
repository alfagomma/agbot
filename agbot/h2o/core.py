
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

class H2o(object):
    """
    H2o core class .
    """
    def __init__(self, profile_name=None):
        """
        Initialize main class.
        """
        logging.info('Init H2o SDK')
        s = Session(profile_name)
        host=s.config.get('agapi_host')
        self.host = f'{host}/h2o'
        self.s = s

    #customer
    def getCustomers(self, query=None):
        """
        Read all customers.
        """
        logging.info('Getting all customers')
        rq = '%s/customer' % (self.host)
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        customer = json.loads(r.text)
        return customer

    def createCustomer(self, payload):
        """
        Create new customer.
        """
        logging.info('Init creating customer...')
        print(payload)
        rq = f'{self.host}/customer'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logging.info('Customer %s created' % customer['data']['id'])
        return customer

    def getCustomer(self, customer_id:int):
        """
        Get customer by id.
        """
        logging.info(f'Reading customer {customer_id}...')        
        rq = f'{self.host}/customer/{customer_id}'
        agent=self.s.getAgent()
        r = agent.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        return customer

    def getCustomerFromErp(self, customer_id, erp_id):
        """
        Read customer from erp external ID
        """
        logging.info(f'Reading customer {customer_id} for erp {erp_id}')
        rq = f'{self.host}/customer/findByErp'
        payload = {
            'erp_id': erp_id, 
            'ext_id': customer_id 
            }
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logging.info('Find customer %s' % customer['data']['id'])
        return customer
    
    def getCustomerFromTax(self, code):
        """
        Read customer from tax code.
        """
        logging.info(f'Reading customer from tax code {code}')
        rq = f'{self.host}/customer/findByTax'
        payload = {
            'code': code
            }
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logging.info('Find customer %s' % customer['data']['id'])
        return customer

    def updateCustomer(self, customer_id:int, payload):
        """
        Update customer data.
        """
        logging.info(f'Updating customer {customer_id}...')
        rq = f'{self.host}/customer/{customer_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        customer = json.loads(r.text)
        logging.info(f'Updated customer {customer_id}')
        return customer

    def createCustomerXerp(self, customer_id:int, payload):
        """
        Update customer ERP Xrefs.
        """
        logging.info(f'Init creating customer {customer_id} ERP xref ...')
        rq = f'{self.host}/customer/{customer_id}/xerp'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
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
        logging.info(f'Creating customer {customer_id} address')
        rq = f'{self.host}/customer/{customer_id}/address'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        address = json.loads(r.text)
        return address

    def updateCustomerAddress(self, customer_id:int, address_id:int, payload):
        """
        Update customer address.
        """
        logging.info(f'Init updating {customer_id} address {address_id} ...')
        rq = f'{self.host}/customer/{customer_id}/address/{address_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        address = json.loads(r.text)
        return address
    
    def getCustomerAddresses(self, customer_id:int, query=None):
        """
        List customer addresses.
        """
        logging.info(f'Getting all customer {customer_id} addresses')
        rq = '{self.host}/customer/{customer_id}/address'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        addresses = json.loads(r.text)
        return addresses

    def getCustomerAddress(self, customer_id:int, address_id:int, params=None):
        """
        Get customer address.
        """
        logging.info(f'Get customer {customer_id} address {address_id}')
        rq = f'{self.host}/customer/{customer_id}/address/{address_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        address = json.loads(r.text)
        return address

    def getCustomerAddressFromExtId(self, customer_id:int, ext_id:str, query=None):
        """
        List customer addresses.
        """
        logging.info(f'Search customer {customer_id} address ext_id {ext_id}.')
        payload ={
            'ext_id' : ext_id
        }
        if query:
            new_payload = dict(item.split("=") for item in query.split('&'))
            payload = {**payload, **new_payload}        
        rq = f'{self.host}/customer/{customer_id}/address/findByExtId'
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
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
        logging.info('Init creating competitor...')
        rq = f'{self.host}/competitor'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        competitor = json.loads(r.text)
        logging.info('Competitor %s created' % competitor['data']['id'])
        return competitor

    def getCompetitor(self, competitor_id:int):
        """
        Get competitor by id.
        """
        logging.info(f'Reading competitor {competitor_id}...')        
        rq = f'{self.host}/competitor/{competitor_id}'
        agent=self.s.getAgent()
        r = agent.get(rq)
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
        logging.info('Creating order %s' % payload)
        rq = f'{self.host}/order'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        logging.info('Order %s created' % order['data']['id'])
        return order

    def getOrders(self, query=None):
        """
        Read all orders.
        """
        logging.info('Getting orders.')
        rq = f'{self.host}/order'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        orders = json.loads(r.text)
        return orders

    def getOrder(self, order_id:int):
        """
        Get order by id
        """
        logging.info(f'Reading order {order_id}..')
        rq = f'{self.host}/order/{order_id}'
        agent=self.s.getAgent()
        r = agent.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        return order        

    def getOrderFromErp(self, erp_id:int, ext_id):
        """
        Read order from erp external ID.
        """
        logging.info(f'Reading order {ext_id} for erp {erp_id}')
        rq = f'{self.host}/order/findByErp'
        payload = {
            'erp_id': erp_id, 
            'ext_id': ext_id 
            }
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        logging.info('Find order %s' % order['data']['id'])
        return order

    def createOrderDetail(self, order_id:int, payload):
        """
        Create order detail.
        """
        logging.info('Creating order detail')
        rq = f'{self.host}/order/{order_id}/detail'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        order = json.loads(r.text)
        return order

    #order type
    def getOrderTypes(self, query=None):
        """
        Read all order types.
        """
        logging.info('Getting order types.')
        rq = f'{self.host}/order/type'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        orderTypes = json.loads(r.text)
        return orderTypes

    def getOrderTypeFromName(self, name:str):
        """
        Get order type by name.
        """
        logging.info('Getting order types.')
        rq = f'{self.host}/order/type/findByName'
        payload={
            'name':name
        }
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            return False
        orderType = json.loads(r.text)
        return orderType        

    def createOrderType(self, payload):
        """
        Create new order type.
        """
        logging.info('Creating new order type.')
        rq = f'{self.host}/order/type'
        agent=self.s.getAgent()
        r = agent.get(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        orderType = json.loads(r.text)
        logging.info(f"Order type {orderType['data']['id']} created")
        return orderType        
