
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SQM SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.2.0"
__date__ = "2019-01-19"

import json
import logging

from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)

class Sqm(object):
    """
    SQM Simple Quality Management core class .
    """
    
    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init SQM SDK')
        s = Session(profile_name)
        host=s.config.get('agapi_host')
        self.host = f'{host}/sqm'
        self.s = s

    def createNorm(self, normName:str):
        """
        Create new norm.
        """
        logger.debug(f'Creating norm {normName}')
        rq = f'{self.host}/norm'
        payload = {'name':normName}
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  
  

    def getNormFromName(self, normName:str):
        """
        Prende la norm dal nome.
        """
        logger.debug(f'Get norm by name {normName}')
        rq = f'{self.host}/norm/findByName'
        payload = {'name':normName}
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)
