
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sqm SDK
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
    
    endpoint = None
    
    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init SQM SDK')
        session = Session(profile_name)
        self.apibot = session.apibot
        self.endpoint = f'{session.ep_agapi}/sqm'


    def createNorm(self, normName:str):
        """
        Create new norm.
        """
        logger.debug('Creating norm %s' % normName)
        rq = '%s/norm' % (self.endpoint)
        payload = {'name':normName}
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  
  

    def getNormFromName(self, normName:str):
        """
        Prende la norm dal nome.
        """
        logger.debug('Get norm by name %s' % normName)
        rq = '%s/norm/findByName' % (self.endpoint)
        payload = {'name':normName}
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)