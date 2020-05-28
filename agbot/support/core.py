
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.0.1"
__date__ = "2020-03-16"

import json, logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)

class Support(object):
    """
    support core class .
    """
    def __init__(self, profile_name=False):
        """
        Initialize main class.
        """
        logger.debug('Init support SDK')
        session = Session(profile_name)
        rqagent =  session.create()
        if not rqagent:
            logger.error('Unable to start support core without valid session.')
            exit(1)
        self.agent = rqagent
        self.host = f'{session.getAgapiHost()}/support'

    #category
    def createCategory(self, payload):
        """
        Create new category.
        """
        logger.debug('Init creating category...')
        rq = f'{self.host}/category'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logger.info('Category %s created' % category['data']['id'])
        return category

    def readCategory(self, category_id:int, query=None):
        """
        Read category.
        """
        logger.debug('Getting category')
        rq = f'{self.host}/category/{category_id}'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category

    def updateCategory(self, category_id, payload):
        """
        Update category data.
        """
        logger.debug(f'Updating category {category_id}...')
        rq = f'{self.host}/category/{category_id}'
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logger.debug(f'Updated category {category_id}')
        return category

    def listCategories(self, query=None):
        """
        Read all categories.
        """
        logger.debug('Getting all categories')
        rq = f'{self.host}/category'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category

    #category type
    def createCategoryType(self, payload):
        """
        Create new category type.
        """
        logger.debug('Init creating category type...')
        rq = f'{self.host}/category/type'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logger.info('Category %s created' % category['data']['id'])
        return category

    def readCategoryType(self, type_id:int, query=None):
        """
        Read category type.
        """
        logger.debug('Read category types')
        rq = f'{self.host}/category/type/{type_id}'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category

    def updateCategoryType(self, type_id, payload):
        """
        Update category type data.
        """
        logger.debug(f'Updating category type {type_id}...')
        rq = f'{self.host}/category/{type_id}'
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        category = json.loads(r.text)
        logger.debug(f'Updated category {type_id}')
        return category

    def listCategoryTypes(self, query=None):
        """
        Read all category types.
        """
        logger.debug('Getting all category types.')
        rq = f'{self.host}/category/type'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        category = json.loads(r.text)
        return category   

    #ticket
    def createTicket(self, payload):
        """
        Create new ticket.
        """
        logger.debug('Init creating ticket...')
        rq = f'{self.host}/ticket'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        ticket = json.loads(r.text)
        logger.info('Ticket %s created' % ticket['data']['id'])
        return ticket

    def readTicket(self, ticket_id:int, query=None):
        """
        Read ticket.
        """
        logger.debug('Read ticket')
        rq = f'{self.host}/ticket/{ticket_id}'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        ticket = json.loads(r.text)
        return ticket

    def updateTicket(self, ticket_id, payload):
        """
        Update ticket.
        """
        logger.debug(f'Updating ticket {ticket_id}...')
        rq = f'{self.host}/ticket/{ticket_id}'
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        ticket = json.loads(r.text)
        logger.debug(f'Updated ticket {ticket_id}')
        return ticket

    def listTicket(self, query=None):
        """
        Read all ticket.
        """
        logger.debug('Getting all ticket.')
        rq = f'{self.host}/ticket'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        tickets = json.loads(r.text)
        return tickets   

