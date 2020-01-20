
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

logger = logging.getLogger()

class Hook(object):
    """
    Hook core class .
    """

    def __init__(self, profile_name=False):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Hook')
        session = Session(profile_name)
        rqagent =  session.create()
        if not rqagent:
            logger.error('Unable to start hook core without valid session.')
            exit(1)
        self.agent = rqagent
        self.host = session.getHookHost()

    #ERP
    def erp_sap_material(self, payload):
        """
        Call erp sap worker queue
        """
        logger.debug(f'Calling erp sap queue')
        rq = f'{self.host}/erp/sap/material'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return True
   
    #ERP SAP CUSTOMER
    def erp_sap_customer(self, payload):
        """
        Call erp sap customer worker queue
        """
        logger.debug(f'Calling erp sap customer queue')
        rq = f'{self.host}/erp/sap/customer'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return True    
