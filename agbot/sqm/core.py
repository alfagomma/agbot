
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQM SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.2.0"
__date__ = "2019-01-19"

import json, logging

from agbot.session import Session, parseApiError

logger = logging.getLogger()

class Sqm(object):
    """
    SQM Simple Quality Management core class .
    """
    
    def __init__(self, profile_name='default'):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init SQM SDK')
        session = Session(profile_name)
        self.agent = session.create()
        self.host = f'{session.agapi_host}/sqm'


    def createNorm(self, normName:str):
        """
        Create new norm.
        """
        logger.debug('Creating norm %s' % normName)
        rq = '%s/norm' % (self.host)
        payload = {'name':normName}
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  
  

    def getNormFromName(self, normName:str):
        """
        Prende la norm dal nome.
        """
        logger.debug('Get norm by name %s' % normName)
        rq = '%s/norm/findByName' % (self.host)
        payload = {'name':normName}
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)