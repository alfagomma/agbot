
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AGCLOUD SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.2"
__date__ = "2019-050-27"

import json
import time
import logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.WARNING)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

class AGCloud(object):
    """
    AGCloud core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init AGCloud')
        session = Session()
        self.apibot = session.apibot
        self.ep_agcloud = session.ep_agcloud

    #erp
    def getErp(self, erp_id:int, params=None):
        """
        Get ERP data.
        """
        logger.debug(f'Get erp {erp_id}')
        rq = f'{self.ep_agcloud}/erp/{erp_id}'
        r = self.apibot.get(rq, params=params)
        if 200 != r.status_code:
            return False
        erp = json.loads(r.text)
        return erp