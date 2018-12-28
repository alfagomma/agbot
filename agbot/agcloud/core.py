
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
        self.ep_agcloud = session.ep_agcloud


    def createNetwork(self, payload):
        """ crea nuovo network """
        logger.debug('Creating new network')
        rq = '%s/network' % (self.ep_agcloud)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _network = json.loads(r.text)
        logger.info('Create network %s' % _network['data']['id'])
        return _network


    def updateNetworkAddress(self, network_id, payload):
        """ Aggiorna indirizzo ad un network """
        logger.debug('Updating network %s address' % network_id)
        rq = '%s/network/%s/address' % (self.ep_agcloud, network_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _address = json.loads(r.text)
        return _address


    def updateNetworkCover(self, network_id, filepath):
        """ send cad file to api """
        logger.debug('Updating network %s cover with %s' % (network_id, filepath))
        rq = '%s/network/%s/cover' % (self.ep_agcloud, network_id)
        cover = {'src': open(filepath, 'rb')}
        try:
            r = self.apibot.post(rq, files=cover)
        except Exception:  # This is the correct syntax
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _network = json.loads(r.text)  
        return _network


    def updateNetworkVideo(self, network_id, payload):
        """ Aggiorna video ad un network """
        logger.debug('Updating network %s video' % network_id)
        rq = '%s/network/%s/video' % (self.ep_agcloud, network_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _network = json.loads(r.text)
        return _network