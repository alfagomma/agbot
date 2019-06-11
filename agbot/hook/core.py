
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hook SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.1"
__date__ = "2019-06-11"

import json, logging, time
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

class Hook(object):
    """
    Hook core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Hook')
        session = Session(profile_name)
        self.apibot = session.apibot
        self.ep_hook = session.ep_hook

    #ERP
    def erp_sap_material(self, payload):
        """
        Call erp sap worker queue
        """
        logger.debug(f'Calling erp sap queue')
        rq = f'{self.ep_hook}/erp/sap/material'
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            return False
        return True

    def erp_sap_customer(self, payload):
        """
        Call erp sap worker queue
        """
        logger.debug(f'Calling erp sap queue')
        rq = f'{self.ep_hook}/erp/sap/customer'
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            return False
        return True        
    
