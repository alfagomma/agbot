
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sqm SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.2.0"
__date__ = "2019-01-19"

import json
import logging
import time

from agbot.session import Session, parseApiError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

class Sqm(object):
    """
    SQM Simple Quality Management core class .
    """
    
    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Sqm')
        session = Session()
        self.apibot = session.apibot
        self.ep_sqm = session.ep_sqm


    def createNorm(self, normName:str):
        """
        Create new norm.
        """
        logger.debug('Creating norm %s' % normName)
        rq = '%s/norm' % (self.ep_sqm)
        payload = {'name':normName}
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  
  

    def getNorm(self, normName:str):
        """
        Prende la norm dal nome.
        """
        logger.debug('Get norm by name %s' % normName)
        rq = '%s/norm/findByName' % (self.ep_sqm)
        payload = {'name':normName}
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)