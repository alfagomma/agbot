
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
H2o SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.3"
__date__ = "2018-10-19"

import json
import logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)

class H2o(object):
    """
    H2o core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init H2o')
        session = Session()
        self.apibot = session.apibot
        self.ep_h2o = session.ep_h2o


    def createOrder(self, payload):
        """
        Create new order
        """
        logger.debug('Creating order %s' % payload)
        rq = '%s/order' % (self.ep_h2o)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _order = json.loads(r.text)
        logger.info('Creating new order %s' % _order['data']['id'])
        return _order


    def getCustomerFromErp(self, customer_id, erp_id):
        """
        Read customer from erp external ID
        """
        logger.debug(f'Reading customer {customer_id} for erp {erp_id}')
        rq = '%s/customer/findByErpId' % (self.ep_h2o)
        payload = {
            'erp_id':erp_id, 
            'ext_id': customer_id 
            }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _customer = json.loads(r.text)
        logger.debug('Find customer %s' % _customer['data']['id'])
        return _customer