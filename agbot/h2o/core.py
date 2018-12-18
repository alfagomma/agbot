
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
        self.ep_element = session.ep_element
        logger.info('Ciao sono H2o')
