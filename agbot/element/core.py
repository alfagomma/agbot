
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Element SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.3"
__date__ = "2018-10-19"

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


    def createNorm(self, normName:str):
        """
        Create new norm.
        """
        logger.debug('Creating norm %s' % normName)
        rq = '%s/norm' % (self.ep_element)
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
        rq = '%s/norm/findByName' % (self.ep_element)
        payload = {'name':normName}
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)  


    def createMaterial(self, payload):
        """
        Create new material.
        """
        logger.debug('Creating material %s' % payload)
        rq = '%s/material' % (self.ep_element)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)


    def getMaterialFromErpId(self, erp_id:int, ext_id:str):
        """
        Get material from ext_id of Erp.
        """
        logger.debug(f'Search material ext_id {ext_id} for erp {erp_id}.')
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
    

    def getMaterialFromErpCode(self, erp_id:int, ext_code:str):
        """
        Get material from ext_code of Erp.
        """
        logger.debug(f'Search material ext_code {ext_code} for erp {erp_id}')
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

    
    def updateMaterial(self, material_id:int, payload):
        """
        Update material.
        """
        logger.debug(f'Updating material {material_id}')
        rq = '%s/material/%s' % (self.ep_element, material_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)


    def syncMaterialNorm(self, material_id:int, payload):
        """
        Sync material norm.
        """
        logger.debug('Sync material %s norm %s' % (material_id, payload))
        rq = '%s/material/%s/norm' % (self.ep_element, material_id)
        r = self.apibot.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False 
        logger.info('Sync material %s norms %s' % (material_id, payload))              
        return True


    def createFamily(self, family_code:str):
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


    def getFamilies(self, query=None):
        """
        Prende tutte le famiglie.
        """
        logger.debug('Getting all the families with query' % query)
        rq = '%s/family' % (self.ep_element)
        r = self.apibot.get(rq, params=query)
        if 200 != r.status_code:
            return False
        _families = json.loads(r.text)
        return _families


    def getFamily(self, family_id:int, params=None):
        """
        Legge la singola famiglia.
        """
        logger.debug(f'Reading family {family_id}')
        rq = '%s/family/%s' % (self.ep_element, family_id)
        r = self.apibot.get(rq, params=params)
        if 200 != r.status_code:
            return False
        _family = json.loads(r.text)
        return _family


    def updateFamily(self, family_id:int, payload):
        """
        Update family.
        """
        logger.debug('Updating family %s ...' % family_id)
        rq = '%s/family/%s' % (self.ep_element, family_id)
        r = self.apibot.post(rq, json=payload) 
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _family = json.loads(r.text)
        return _family        
        

    def getFamilyFromCode(self, family_code:str):
        """ Prende famiglia da nome """
        logger.debug('Get family %s' % family_code)
        rq = '%s/family/findByCode' % (self.ep_element)
        payload = {'code': family_code}
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)    


    def patchFamilyProduct(self, family_id:int, product_id:int):
        """
        Sincronizza il prodotto con la famiglia
        """
        logger.debug(f'Pathing family {family_id} with product {product_id}')
        rq = '%s/family/%s' % (self.ep_element, family_id)
        payload = {
            'product_id': product_id
            }
        try:
            r = self.apibot.patch(rq, json=payload)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)


    def updateFamilyCover(self, family_id:int, localFile):
        """ 
        Aggiorna cover famiglia. 
        """
        logger.debug('Update family %s cover with file %s' % (family_id, localFile))
        rq = '%s/family/%s/cover' % (self.ep_element, family_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        #files = {'src': ('test.cad', open(filepath, 'rb'), 'image/png')}
        try:
            r = self.apibot.post(rq, files=files)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _family = json.loads(r.text)
        return _family


    def attachFamilyNorm(self, family_id:int, norm_id:int):
        """
        Aggiunge una norma riconosciuta, alla famiglia
        """
        logger.debug('Attach norm %s at family %s' % (norm_id, family_id))
        rq = '%s/family/%s/norm' % (self.ep_element, family_id)
        payload = {
            'norm_id' : norm_id
            }
        r = self.apibot.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True


    def attachFamilyQuality(self, family_id:int, quality_id:int):
        """
        Aggiunge una qualità alla famiglia
        """
        logger.debug('Attach quality %s at family %s' % (quality_id, family_id))
        rq = '%s/family/%s/quality' % (self.ep_element, family_id)
        payload = {
            'quality_id' : quality_id
            }
        r = self.apibot.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True        


    def attachFamilyFeature(self, family_id:int, feature_id:int, description:str):
        """
        Aggiunge una feature alla famiglia.
        """
        logger.debug('Attaching feature %s at family %s' % (family_id, feature_id) )
        payload = {
            'feature_id': feature_id,
            'description': description
        }
        rq = '%s/family/%s/feature' % (self.ep_element, family_id)
        try:
            r = self.apibot.post(rq, json=payload)
        except Exception:
            logger.exception('Exception occured')
            return False
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True


    def createFeature(self, feature_name:str):
        """
        Crea una nuova feature.
        """
        logger.debug('Creating new feature with name %s' % feature_name)
        rq = '%s/feature' % (self.ep_element)
        payload = {
            'name' : feature_name
            }
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _feature = json.loads(r.text)
        return _feature


    def getFeature(self, feature_name:str):
        """
        Prende feature dal nome.
        """
        logger.debug('Getting feature by name %s...' % feature_name)
        params = {
            'name' : feature_name
        }
        rq = '%s/feature/findByName' % (self.ep_element)
        r = self.apibot.get(rq, params=params)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _features = json.loads(r.text)
        return _features


    def getDivisionByName(self, division_name:str):
        """ 
        Prende divisione da nome.
        """
        logger.debug('Search division by name %s' % division_name)
        rq = '%s/division/findByName?name=%s' % (self.ep_element, division_name)
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _division = json.loads(r.text)
        return _division


    def createDivision(self, division_name:str):
        """ 
        Crea una divisione.
        """
        logger.debug('Creating new division with name %s' % division_name)
        rq = '%s/division' % (self.ep_element)
        payload = {'name':division_name}
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _division = json.loads(r.text)
        return _division


    def createProduct(self, division_id:int, product_name:str):
        """
        Crea un prodotto.
        """
        logger.debug('Creating new product with name %s at division %s' % (product_name, division_id))
        rq = '%s/product' % (self.ep_element)
        payload = {
            'division_id': division_id,
            'name':product_name
            }
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _product = json.loads(r.text)
        return _product


    def getProductByName(self, product_name:str):
        """
        Prende prodotto da nome.
        """
        logger.debug('Search product by name %s' % product_name)
        rq = '%s/product/findByName?name=%s' % (self.ep_element, product_name)
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _product = json.loads(r.text)
        return _product


    def updateProductCover(self, product_id:int, localFile):
        """
        Aggiorna cover prodotto.
        """
        logger.debug('Update product %s cover with file %s' % (product_id, localFile))
        rq = '%s/product/%s/cover' % (self.ep_element, product_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        try:
            r = self.apibot.post(rq, files=files)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _product = json.loads(r.text)        
        return _product
