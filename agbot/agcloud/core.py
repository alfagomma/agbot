
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AGCLOUD SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.3"
__date__ = "2018-10-19"

import json
import time
import logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)

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
        self.ep_element = session.ep_element
