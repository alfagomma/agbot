
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BASE SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.1"
__date__ = "2019-11-07"

import json, logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)

class Base(object):
    """
    AGCloud BASE Data core class .
    """

    def __init__(self, profile_name=False):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Base SDK')
        session = Session(profile_name)
        rqagent =  session.create()
        if not rqagent:
            logger.error('Unable to start base core without valid session.')
            exit(1)
        self.agent = rqagent
        self.host = session.getAgapiHost()

    #erp
    def getErp(self, erp_id:int, params=None):
        """
        Get ERP data.
        """
        logger.debug(f'Get erp {erp_id}')
        rq = f'{self.host}/erp/{erp_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        erp = json.loads(r.text)
        return erp

    #unit of measure
    def getUoms(self, query=None):
        """Get all uoms."""
        logger.debug('Getting all unit of measure...')
        rq = f'{self.host}/unitofmeasure'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        uoms = json.loads(r.text)
        return uoms

    def getUom(self, uom_id:int, query=None):
        """
        Leggo uom da id.
        """
        logger.debug(f'Reading family {uom_id}...')
        rq = f'{self.host}/unitofmeasure/{uom_id}'
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        uom = json.loads(r.text)
        return uom

    def getUomFromCode(self, code:str, query=None):
        """
        Leggo uom da code.
        """
        logger.debug(f'Reading uom code {code}...')
        params = {
            'code': code
            }
        if query:
            new_params = dict(item.split("=") for item in query.split('&'))
            params = {**params, **new_params}     
        rq = f'{self.host}/unitofmeasure/findByCode'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        uom = json.loads(r.text)
        return uom        
