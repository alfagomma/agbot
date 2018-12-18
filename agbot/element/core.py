
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Element SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.3"
__date__ = "2018-10-19"

import json
import time
import logging
from agbot.session import Session, parseApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('logs/element%s.log' % (time.strftime("%Y%m%d")))
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.WARNING)
# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)

class Element(object):
    """
    Element core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Element')
        session = Session()
        self.apibot = session.apibot
        self.ep_element = session.ep_element


    def createFamily(self, family_code):
        """ crea una nuova famiglia """
        logger.debug('Creating new family %s' % family_code)
        rq = '%s/family' % (self.ep_element)
        payload = {
            'code': family_code
            }
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _family = json.loads(r.text)
        logger.info('Create family %s' % _family['data']['id'])
        return _family


    def getFamilyFromCode(self, family_code):
        """ Prende famiglia da nome """
        logger.debug('Get family %s' % family_code)
        rq = '%s/family/findByCode' % (self.ep_element)
        payload = {'code': family_code}
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)    


    def createNorm(self, normName):
        """ create new norm """
        logger.debug('Creating norm %s' % normName)
        rq = '%s/norm' % (self.ep_element)
        payload = {'name':normName}
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  
  

    def getNorm(self, normName):
        """ prende la normNamea dal nome """
        logger.debug('Get norm by name %s' % normName)
        rq = '%s/norm/findByName' % (self.ep_element)
        payload = {'name':normName}
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  


    def createMaterial(self, payload):
        """ Create new material """
        logger.debug('Creating material %s' % payload)
        rq = '%s/material' % (self.ep_element)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)


    def getMaterialFromErpId(self, erp_id, ext_id):
        """ Get material from ext_id of Erp """
        rq = '%s/material/findByErpId' % (self.ep_element)
        payload = {
            'erp_id' : erp_id,
            'ext_id' : ext_id
        }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 
    

    def getMaterialFromErpCode(self, erp_id, ext_code):
        """ Get material from ext_code of Erp """
        rq = '%s/material/findByErpCode' % (self.ep_element)
        payload = {
            'erp_id' : erp_id,
            'ext_code' : ext_code
        }
        r = self.apibot.post(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    
    def updateMaterial(self, material_id, payload):
        """ Update material """
        rq = '%s/material/%s' % (self.ep_element, material_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)


    def syncMaterialNorm(self, material_id, payload):
        """ sync material norm """
        logger.debug('Sync material %s norm %s' % (material_id, payload))
        rq = '%s/material/%s/norm' % (self.ep_element, material_id)
        r = self.apibot.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False 
        logger.info('Sync material %s norms %s' % (material_id, payload))              