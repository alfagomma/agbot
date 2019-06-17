
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Element SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.2.2"
__date__ = "2019-06-08"

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

class Element(object):
    """
    Element core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Element')
        session = Session(profile_name)
        self.apibot = session.apibot
        self.ep_element = session.ep_element

    #item
    def getItem(self, item_id:int, params=None):
        """
        Legge un item dal suo id.
        """
        logger.debug(f'Get item {item_id}')
        rq = f'{self.ep_element}/item/{item_id}'
        r = self.apibot.get(rq, params=params)
        if 200 != r.status_code:
            return False
        item = json.loads(r.text)
        return item

    def getItems(self, query=None):
        """
        Prende tutti gli items.
        """
        logger.debug('Getting all the items')
        rq = '%s/item' % (self.ep_element)
        r = self.apibot.get(rq, params=query)
        if 200 != r.status_code:
            return False
        _items = json.loads(r.text)
        return _items

    def createItem(self, payload):
        """
        Create new item.
        """
        logger.debug('Creating item %s' % payload)
        rq = '%s/item' % (self.ep_element)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        item = json.loads(r.text)
        logger.info('Create item %s' % item['data']['id'])
        return item

    def getItemFromExt_id(self, ext_id:int, params=None):
        """
        Get item from ext_id.
        """
        logger.debug(f'Search item ext_id {ext_id}.')
        payload ={
            'ext_id' : ext_id
        }
        if params:
            new_payload = dict(item.split("=") for item in params.split('&'))
            payload = {**payload, **new_payload}        
        rq = '%s/item/findByExtId' % (self.ep_element)
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def getItemFromCode(self, item_code:str):
        """
        Get item from code
        """
        logger.debug(f'Search item code {item_code}.')
        payload ={
            'code' : item_code
        }     
        rq = '%s/item/findByCode' % (self.ep_element)
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def getItemFromErpId(self, erp_id:int, ext_id:str):
        """
        Get item from ext_id of Erp.
        """
        logger.debug(f'Search item ext_id {ext_id} for erp {erp_id}.')
        rq = '%s/item/findByErpExtId' % (self.ep_element)
        payload = {
            'erp_id' : erp_id,
            'ext_id' : ext_id
        }
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def updateItem(self, item_id:int, payload):
        """
        Update item.
        """
        logger.debug(f'Updating item {item_id} with {payload}')
        rq = '%s/item/%s' % (self.ep_element, item_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def patchItem(self, item_id:int, payload):
        """
        Patch know item field.
        """
        logger.debug(f'Patching item {item_id} with {payload}')
        rq = '%s/item/%s' % (self.ep_element, item_id)
        r = self.apibot.patch(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        item = json.loads(r.text)        
        return item

    def createItemAttribute(self, item_id:int, payload):
        """
        Create new item attributes.
        """
        logger.debug(f'Creating item {item_id} attributes {payload}')
        rq = '%s/item/%s/attribute' % (self.ep_element, item_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def syncItemNorm(self, item_id:int, payload):
        """
        Sync item norm.
        """
        logger.debug(f'Sync item {item_id} norm {payload}')
        rq = '%s/item/%s/norm' % (self.ep_element, item_id)
        r = self.apibot.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False 
        logger.info(f'Sync item {item_id} norms complete')              
        return True

    def syncItemCatalogs(self, item_id:int, payload):
        """
        Sync item catalogs.
        """
        logger.debug('Sync item %s catalogs %s' % (item_id, payload))
        rq = '%s/item/%s/catalog/sync' % (self.ep_element, item_id)
        r = self.apibot.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        logger.info(f'Sync item {item_id} catalogs complete')              
        return True

    def itemAddCad(self, item_id:int, localFile):
        """ 
        Aggiunge un file cad all'item. 
        """
        logger.debug('')
        rq = '%s/item/%s/cad' % (self.ep_element, item_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        try:
            r = self.apibot.post(rq, files=files)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 201 != r.status_code:
            parseApiError(r)
            return False
        cad = json.loads(r.text)
        return cad

    def itemDeleteCad(self, item_id:int, cad_id:int):
        """ 
        Elimina un file cad dall'item. 
        """
        logger.debug('')
        rq = f'{self.ep_element}/item/{item_id}/cad/{cad_id}'
        try:
            r = self.apibot.delete(rq)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    #family
    def createFamily(self, payload):
        """ crea una nuova famiglia """
        logger.debug('Creating new family %s' % payload)
        rq = '%s/family' % (self.ep_element)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        family = json.loads(r.text)
        logger.info('Create family %s' % family['data']['id'])
        return family

    def getFamilies(self, query=None):
        """
        Prende tutte le famiglie.
        """
        logger.debug('Getting all the families')
        rq = '%s/family' % (self.ep_element)
        r = self.apibot.get(rq, params=query)
        if 200 != r.status_code:
            return False
        families = json.loads(r.text)
        return families

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

    def getFamilyFromCode(self, family_code:str, params=None):
        """ Prende famiglia da nome """
        payload ={
            'code' : family_code
        }
        if params:
            new_payload = dict(item.split("=") for item in params.split('&'))
            payload = {**payload, **new_payload}
        logger.debug('Get family %s' % family_code)
        rq = '%s/family/findByCode' % (self.ep_element)
        r = self.apibot.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)    

    def patchFamilyCategory(self, family_id:int, category_id:int):
        """
        Associa categoria a famiglia
        """
        logger.debug(f'Patching family {family_id} with category {category_id}')
        rq = '%s/family/%s' % (self.ep_element, family_id)
        payload = {
            'category_id': category_id
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

    def patchFamilyDatasheet(self, family_id:int, datasheet_id:int):
        """
        Associa datasheet a famiglia
        """
        logger.debug(f'Pathing family {family_id} with datasheet {datasheet_id}')
        rq = '%s/family/%s' % (self.ep_element, family_id)
        payload = {
            'datasheet_id': datasheet_id
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

    def updateFamilyHq(self, family_id:int, localFile):
        """ 
        Aggiorna HQ famiglia. 
        """
        logger.debug('Update family %s hq with file %s' % (family_id, localFile))
        rq = '%s/family/%s/hq' % (self.ep_element, family_id)
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
        Aggiunge una norma riconosciuta, alla famiglia.
        SUGGEST - USE syncFamilyNorm!
        """
        logger.debug('Attaching norm %s at family %s ...' % (norm_id, family_id))
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
        SUGGEST - USE syncFamilyNorm!
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
        logger.debug('Attaching feature %s at family %s' % (feature_id, family_id) )
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

    #feature
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

    #division
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

    #category
    def createCategory(self, division_id:int, category_name:str):
        """
        Crea un categoria.
        """
        logger.debug('Creating new category with name %s at division %s' % (category_name, division_id))
        rq = '%s/category' % (self.ep_element)
        payload = {
            'division_id': division_id,
            'name':category_name
            }
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _category = json.loads(r.text)
        return _category

    def getCategoryByName(self, category_name:str):
        """
        Prende categoria da nome.
        """
        logger.debug('Search category by name %s' % category_name)
        rq = '%s/category/findByName?name=%s' % (self.ep_element, category_name)
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _category = json.loads(r.text)
        return _category

    def updateCategoryCover(self, category_id:int, localFile):
        """
        Aggiorna cover categoria.
        """
        logger.debug('Update category %s cover with file %s' % (category_id, localFile))
        rq = '%s/category/%s/cover' % (self.ep_element, category_id)
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
        _category = json.loads(r.text)        
        return _category

    #datasheet
    def createDatasheet(self, payload):
        """
        Create new datasheet.
        """
        logger.debug('Creating datasheet %s' % payload)
        rq = '%s/datasheet' % (self.ep_element)
        r = self.apibot.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def getDatasheetByName(self, datasheet_name:str):
        """ 
        Prende griglia da nome.
        """
        logger.debug('Search datasheet by name %s' % datasheet_name)
        rq = '%s/datasheet/findByName?name=%s' % (self.ep_element, datasheet_name)
        r = self.apibot.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        datasheet = json.loads(r.text)
        return datasheet

    def updateDatasheet(self, datasheet_id:int, payload):
        """
        Update datasheet.
        """
        logger.debug(f'Updating datasheet {datasheet_id}')
        rq = '%s/datasheet/%s' % (self.ep_element, datasheet_id)
        r = self.apibot.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        datasheet = json.loads(r.text)
        return datasheet

    #unit of measure
    def getUoms(self, query=None):
        """Get all uoms."""
        logger.debug('Getting all unit of measure...')
        rq = f'{self.ep_element}/unitofmeasure'
        r = self.apibot.get(rq, params=query)
        if 200 != r.status_code:
            return False
        uoms = json.loads(r.text)
        return uoms

    def getUom(self, uom_id:int, query=None):
        """
        Leggo uom da id.
        """
        logger.debug(f'Reading family {uom_id}...')
        rq = f'{self.ep_element}/unitofmeasure/{uom_id}'
        r = self.apibot.get(rq, params=query)
        if 200 != r.status_code:
            return False
        uom = json.loads(r.text)
        return uom

    def getUomFromCode(self, code:str, query=None):
        """
        Leggo uom da code.
        """
        logger.debug(f'Reading uom code {code}...')
        params = {
            'code': code
            }
        if query:
            new_params = dict(item.split("=") for item in query.split('&'))
            params = {**params, **new_params}     
        rq = f'{self.ep_element}/unitofmeasure/findByCode'
        r = self.apibot.get(rq, params=params)
        if 200 != r.status_code:
            return False
        uom = json.loads(r.text)
        return uom        
