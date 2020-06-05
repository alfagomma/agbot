
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.0.1"
__date__ = "2020-03-16"

import json
import logging

from agbot.session import Session, parseApiError

class Support(object):
    """
    support core class .
    """
    def __init__(self, profile_name=None):
        """
        Initialize main class.
        """
        logging.info('Init support SDK')
        s = Session(profile_name)
        host=s.config.get('agapi_host')
        self.host = f'{host}/support'
        self.s = s
        
    #category
    def createCategory(self, payload:object):
        """
        Create new category.
        """
        logging.info('Init creating category...')
        rq = f'{self.host}/category'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logging.info('Category %s created' % category['data']['id'])
        return category

    def readCategory(self, category_id:int, query=None):
        """
        Read category.
        """
        logging.info('Getting category')
        rq = f'{self.host}/category/{category_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category

    def updateCategory(self, category_id:int, payload:object):
        """
        Update category data.
        """
        logging.info(f'Updating category {category_id}...')
        rq = f'{self.host}/category/{category_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logging.info(f'Updated category {category_id}')
        return category

    def listCategories(self, query=None):
        """
        Read all categories.
        """
        logging.info('Getting all categories')
        rq = f'{self.host}/category'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        return category

    #category type
    def createCategoryType(self, payload):
        """
        Create new category type.
        """
        logging.info('Init creating category type...')
        rq = f'{self.host}/category/type'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logging.info('Category %s created' % category['data']['id'])
        return category

    def readCategoryType(self, type_id:int, query=None):
        """
        Read category type.
        """
        logging.info('Read category types')
        rq = f'{self.host}/category/type/{type_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category

    def updateCategoryType(self, type_id, payload):
        """
        Update category type data.
        """
        logging.info(f'Updating category type {type_id}...')
        rq = f'{self.host}/category/{type_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logging.info(f'Updated category {type_id}')
        return category

    def listCategoryTypes(self, query=None):
        """
        Read all category types.
        """
        logging.info('Getting all category types.')
        rq = f'{self.host}/category/type'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category   

    #ticket
    def createTicket(self, payload):
        """
        Create new ticket.
        """
        logging.info('Init creating ticket...')
        rq = f'{self.host}/ticket'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        ticket = json.loads(r.text)
        logging.info('Ticket %s created' % ticket['data']['id'])
        return ticket

    def readTicket(self, ticket_id:int, query=None):
        """
        Read ticket.
        """
        logging.info('Read ticket')
        rq = f'{self.host}/ticket/{ticket_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        ticket = json.loads(r.text)
        return ticket

    def updateTicket(self, ticket_id, payload):
        """
        Update ticket.
        """
        logging.info(f'Updating ticket {ticket_id}...')
        rq = f'{self.host}/ticket/{ticket_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        ticket = json.loads(r.text)
        logging.info(f'Updated ticket {ticket_id}')
        return ticket

    def listTicket(self, query=None):
        """
        Read all ticket.
        """
        logging.info('Getting all ticket.')
        rq = f'{self.host}/ticket'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        tickets = json.loads(r.text)
        return tickets   
