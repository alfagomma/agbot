
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Element SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.1"
__date__ = "2019-11-04"

import json
import logging
import time

from agbot.session import Session, parseApiError

class Element(object):
    """
    Element core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logging.info('Init Element SDK')
        s = Session(profile_name)
        host=s.config.get('agapi_host')
        self.host = f'{host}/element'
        self.s = s

    #item
    def getItem(self, item_id:int, params=None):
        """
        Legge un item dal suo id.
        """
        logging.info(f'Get item {item_id}')
        rq = f'{self.host}/item/{item_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        item = json.loads(r.text)
        return item

    def getItems(self, query=None):
        """
        Prende tutti gli items.
        """
        logging.info('Getting all the items')
        rq = '%s/item' % (self.host)
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        _items = json.loads(r.text)
        return _items

    def createItem(self, payload):
        """
        Create new item.
        """
        logging.info('Creating item %s' % payload)
        rq = '%s/item' % (self.host)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        item = json.loads(r.text)
        logging.info('Create item %s' % item['data']['id'])
        return item

    def getItemFromExt_id(self, ext_id:str, params={}):
        """
        Get item from ext_id.
        """
        logging.info(f'Search item ext_id {ext_id}.')
        payload ={
            'ext_id' : ext_id
        }
        if params:payload.update(params)
        rq = f'{self.host}/item/findByExtId'
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def getItemFromCode(self, item_code:str, params=None):
        """
        Get item from code
        """
        logging.info(f'Search item code {item_code}.')
        payload ={
            'code' : item_code
        }
        if params:
            new_payload = dict(item.split("=") for item in params.split('&'))
            payload = {**payload, **new_payload}
        rq = f'{self.host}/item/findByCode'
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def getItemFromErpId(self, erp_id:int, ext_id:str):
        """
        Get item from ext_id of Erp.
        """
        logging.info(f'Search item ext_id {ext_id} for erp {erp_id}.')
        rq = '%s/item/findByErpExtId' % (self.host)
        payload = {
            'erp_id' : erp_id,
            'ext_id' : ext_id
        }
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def updateItem(self, item_id:int, payload):
        """
        Update item.
        """
        logging.info(f'Updating item {item_id} with {payload}')
        rq = '%s/item/%s' % (self.host, item_id)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def patchItem(self, item_id:int, payload):
        """
        Patch know item field.
        """
        logging.info(f'Patching item {item_id} with {payload}')
        rq = '%s/item/%s' % (self.host, item_id)
        agent=self.s.getAgent()
        r = agent.patch(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        item = json.loads(r.text)        
        return item

    def createItemAttribute(self, item_id:int, payload):
        """
        Create new item attributes.
        """
        logging.info(f'Creating item {item_id} attributes {payload}')
        rq = '%s/item/%s/attribute' % (self.host, item_id)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def syncItemNorm(self, item_id:int, payload):
        """
        Sync item norm.
        """
        logging.info(f'Sync item {item_id} norm {payload}')
        rq = '%s/item/%s/norm' % (self.host, item_id)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False 
        logging.info(f'Sync item {item_id} norms complete')              
        return True

    def itemAddCad(self, item_id:int, localFile):
        """ 
        Aggiunge un file cad all'item. 
        """
        logging.info('')
        rq = '%s/item/%s/cad' % (self.host, item_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        try:
            agent=self.s.getAgent()
            r = agent.post(rq, files=files)
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
        logging.info('')
        rq = f'{self.host}/item/{item_id}/cad/{cad_id}'
        try:
            agent=self.s.getAgent()
            r = agent.delete(rq)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def itemAddCompetitor(self, item_id:int, payload):
        """ attach warehouse to the item"""
        logging.info(f'Add xref item {item_id} {payload}')
        rq = f'{self.host}/item/{item_id}/xcompetitor'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        return True

    def itemUpdateCompetitor(self, item_id:int, xref_id:int, code):
        """ update item competitor cross reference"""
        logging.info(f'Update competitor {xref_id} with code {code}')
        payload={
            'code': code
        }
        rq = f'{self.host}/item/{item_id}/xcompetitor/{xref_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return True

    def itemDeleteCompetitor(self, item_id:int, competitor_id:int):
        """ Remove item competitor cross reference"""
        logging.info(f'Removing competitor {competitor_id} from item {item_id}')
        rq = f'{self.host}/item/{item_id}/xcompetitor/{competitor_id}'
        agent=self.s.getAgent()
        r = agent.delete(rq)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def itemAddWarehouse(self, item_id:int, payload):
        """ attach warehouse to the item"""
        logging.info(f'Add warehouse at {item_id} - {payload}')
        rq = f'{self.host}/item/{item_id}/warehouse'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def itemRemoveWarehouse(self, item_id:int, warehouse_id:int):
        """ attach warehouse to the item"""
        logging.info(f'Remove warehouse {warehouse_id} @ item {item_id}')
        rq = f'{self.host}/item/{item_id}/warehouse/{warehouse_id}'
        agent=self.s.getAgent()
        r = agent.delete(rq)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def itemPatchWarehouse(self, item_id:int, warehouse_id:int, payload):
        """ attach warehouse to the item"""
        logging.info(f'Patching item {item_id}@warehouse {warehouse_id} - {payload}')
        rq = f'{self.host}/item/{item_id}/warehouse/{warehouse_id}'
        agent=self.s.getAgent()
        r = agent.patch(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True        

    #attribute
    def createAttribute(self, payload):
        """ crea un nuovo attributo """
        logging.info('Creating new attribute %s' % payload)
        rq = f'{self.host}/attribute'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        attribute = json.loads(r.text)
        logging.info('Create attribute %s' % attribute['data']['id'])
        return attribute

    def getAttributes(self, query=None):
        """
        Read all attributes.
        """
        logging.info('Getting all the attributes.')
        rq = f'{self.host}/attribute'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        attributes = json.loads(r.text)
        return attributes

    def getAttribute(self, attribute_id:int, params=None):
        """ Attribute by id """
        logging.info(f'Get attribute {attribute_id}')
        rq = f'{self.host}/attribute/{attribute_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def getAttributeByName(self, attribute_name:str, params=None):
        """ Attribute by name """
        payload ={
            'name' : attribute_name
        }
        if params:
            new_payload = dict(item.split("=") for item in params.split('&'))
            payload = {**payload, **new_payload}
        logging.info(f'Get attribute {attribute_name}')
        rq = f'{self.host}/attribute/findByName'
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def updateAttribute(self, attribute_id:int, payload):
        """
        Update attribute.
        """
        logging.info(f'Updating attribute {attribute_id} ...')
        rq = f'{self.host}/attribute/{attribute_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload) 
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _family = json.loads(r.text)
        return _family 

    #family
    def createFamily(self, payload):
        """ crea una nuova famiglia """
        logging.info('Creating new family %s' % payload)
        rq = '%s/family' % (self.host)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        family = json.loads(r.text)
        logging.info('Create family %s' % family['data']['id'])
        return family

    def getFamilies(self, params=None):
        """
        Prende tutte le famiglie.
        """
        logging.info(f'Getting all the families with params {params}')
        rq = '%s/family' % (self.host)
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        families = json.loads(r.text)
        return families

    def getFamily(self, family_id:int, params=None):
        """
        Legge la singola famiglia.
        """
        logging.info(f'Reading family {family_id}')
        rq = '%s/family/%s' % (self.host, family_id)
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        _family = json.loads(r.text)
        return _family

    def updateFamily(self, family_id:int, payload):
        """
        Update family.
        """
        logging.info('Updating family %s ...' % family_id)
        rq = '%s/family/%s' % (self.host, family_id)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload) 
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
        logging.info('Get family %s' % family_code)
        rq = '%s/family/findByCode' % (self.host)
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)    

    def patchFamily(self, family_id:int, payload):
        """
        Associa categoria a famiglia
        """
        logging.info(f'Patching family {family_id} ')
        rq = '%s/family/%s' % (self.host, family_id)
        try:
            agent=self.s.getAgent()
            r = agent.patch(rq, json=payload)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def patchFamilyCategory(self, family_id:int, category_id:int):
        """
        Associa categoria a famiglia
        """
        logging.info(f'Patching family {family_id} with category {category_id}')
        rq = '%s/family/%s' % (self.host, family_id)
        payload = {
            'category_id': category_id
            }
        try:
            agent=self.s.getAgent()
            r = agent.patch(rq, json=payload)
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
        logging.info('Update family %s cover with file %s' % (family_id, localFile))
        rq = '%s/family/%s/cover' % (self.host, family_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        #files = {'src': ('test.cad', open(filepath, 'rb'), 'image/png')}
        try:
            agent=self.s.getAgent()
            r = agent.post(rq, files=files)
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
        logging.info('Update family %s hq with file %s' % (family_id, localFile))
        rq = '%s/family/%s/hq' % (self.host, family_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        #files = {'src': ('test.cad', open(filepath, 'rb'), 'image/png')}
        try:
            agent=self.s.getAgent()
            r = agent.post(rq, files=files)
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
        logging.info(f'Attaching norm {norm_id} at family {family_id} ...')
        rq = f"{self.host}/family/{family_id}/norm"
        payload = {
            'norm_id' : norm_id
            }
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def attachFamilyQuality(self, family_id:int, quality_id:int):
        """
        Aggiunge una qualità alla famiglia
        SUGGEST - USE syncFamilyNorm!
        """
        logging.info(f'Attach quality {quality_id} at family {family_id}')
        rq = f'{self.host}/family/{family_id}/quality'
        payload = {
            'quality_id' : quality_id
            }
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True        

    def attachFamilyFeature(self, family_id:int, feature_id:int, description:str):
        """
        Aggiunge una feature alla famiglia.
        """
        logging.info('Attaching feature %s at family %s' % (feature_id, family_id) )
        payload = {
            'feature_id': feature_id,
            'description': description
        }
        rq = f'{self.host}/family/{family_id}/feature'
        try:
            agent=self.s.getAgent()
            r = agent.post(rq, json=payload)
        except Exception:
            logging.exception('Exception occured')
            return False
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def attachFamilyAttribute(self, family_id:int, attribute_id:int):
        """
        Add attribute to family.
        """
        logging.info(f'Attaching attribute {attribute_id} to family {family_id}...')
        rq = f'{self.host}/family/{family_id}/attribute'
        payload = {
            'attribute_id' : attribute_id
            }
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def attachFamilySorting(self, family_id:int, attribute_id:int):
        """
        Add attribute to sorting
        """
        logging.info(f'Attaching attribute {attribute_id} to family {family_id} sorting...')
        rq = f'{self.host}/family/{family_id}/sorting'
        payload = {
            'attribute_id' : attribute_id
            }
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    #feature
    def createFeature(self, feature_name:str):
        """
        Crea una nuova feature.
        """
        logging.info(f'Creating new feature with name {feature_name}')
        rq = f'{self.host}/feature'
        payload = {
            'name' : feature_name
            }
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _feature = json.loads(r.text)
        return _feature

    def getFeature(self, feature_name:str):
        """
        Prende feature dal nome.
        """
        logging.info('Getting feature by name %s...' % feature_name)
        params = {
            'name' : feature_name
        }
        rq = f'{self.host}/feature/findByName'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _features = json.loads(r.text)
        return _features

    #crtable
    def createCrtable(self, payload):
        """ crea una nuova tabella """
        logging.info('Creating new crtabel %s' % payload)
        rq = '%s/crtable' % (self.host)
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        crtable = json.loads(r.text)
        logging.info('Create crtable %s' % crtable['data']['id'])
        return crtable

    def getCrtable(self, crtable_id:int, params=None):
        """
        Legge una tabella dal suo id.
        """
        logging.info(f'Get crtable {crtable_id}')
        rq = f'{self.host}/crtable/{crtable_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable

    def getCrtableFromSlug(self, slug:str):
        """
        Legge una tabella dal suo slug.
        """
        logging.info(f'Get crtable slug {slug}')
        rq = f'{self.host}/crtable/findBySlug'
        agent=self.s.getAgent()
        r = agent.get(rq, params={
            'slug' : slug
        })
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable

    def getCrtableFromName(self, name:str):
        """
        Legge una tabella dal suo name.
        """
        logging.info(f'Get crtable name {name}')
        rq = f'{self.host}/crtable/findByName'
        agent=self.s.getAgent()
        r = agent.get(rq, params={
            'name' : name
        })
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable


    #crimping
    def createCrimping(self, crtable_id:int, payload):
        """ crea nuovo parametro di pinzatura per tabella """
        logging.info('Creating new crimping %s' % payload)
        rq = f'{self.host}/crtable/{crtable_id}/crimping'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        crimping = json.loads(r.text)
        logging.info('Create crimping %s' % crimping['data']['id'])
        return crimping

    def getCrimping(self, crtable_id:int, crimping_id:int, params=None):
        """
        Legge un parametro dalla tabella pinzatura.
        """
        logging.info(f'Get crimping {crimping_id} from table {crtable_id}')
        rq = f'{self.host}/crtable/{crtable_id}/crimping/{crimping_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable

    #hub
    def getHubByName(self, hub_name:str):
        """ 
        Get hub from name
        """
        logging.info('Search hub by name %s' % hub_name)
        rq = f'{self.host}/hub/findByName?name={hub_name}'
        agent=self.s.getAgent()
        r = agent.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _hub = json.loads(r.text)
        return _hub

    def createHub(self, hub_name:str):
        """ 
        Create new hub
        """
        logging.info('Creating new hub with name %s' % hub_name)
        rq = f'{self.host}/hub'
        payload = {'name':hub_name}
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _hub = json.loads(r.text)
        return _hub

    #category
    def createCategory(self, hub_id:int, category_name:str):
        """
        Crea un categoria.
        """
        logging.info('Creating new category with name %s at hub %s' % (category_name, hub_id))
        rq = '%s/category' % (self.host)
        payload = {
            'hub_id': hub_id,
            'name':category_name
            }
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        _category = json.loads(r.text)
        return _category

    def getCategoryByName(self, category_name:str):
        """
        Prende categoria da nome.
        """
        logging.info('Search category by name %s' % category_name)
        rq = '%s/category/findByName?name=%s' % (self.host, category_name)
        agent=self.s.getAgent()
        r = agent.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _category = json.loads(r.text)
        return _category

    def updateCategoryCover(self, category_id:int, localFile):
        """
        Aggiorna cover categoria.
        """
        logging.info('Update category %s cover with file %s' % (category_id, localFile))
        rq = '%s/category/%s/cover' % (self.host, category_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        try:
            agent=self.s.getAgent()
            r = agent.post(rq, files=files)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _category = json.loads(r.text)        
        return _category

    #catalog
    def listCatalog(self, query=None):
        """ Get catalog by ID """
        logging.info(f'List catalogs')
        rq = f'{self.host}/catalog'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        logging.info(r)
        if 200 != r.status_code:
            return False
        catalogs = json.loads(r.text)
        return catalogs

    def getCatalog(self, catalog_id:int, params=None):
        """ Get catalog by ID """
        logging.info(f'Get catalog {catalog_id}')
        rq = f'{self.host}/catalog/{catalog_id}'
        logging.info(rq)
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        logging.info(r)
        if 200 != r.status_code:
            return False
        item = json.loads(r.text)
        return item

    def getTree(self, catalog_id:int, tree_id:int, params=None):
        """ Get catalog tree by ID """
        logging.info(f'Get catalog tree {catalog_id}')
        rq = f'{self.host}/catalog/{catalog_id}/tree/{tree_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        tree = json.loads(r.text)
        return tree    

    def getTreeLeaves(self, catalog_id:int, params=None):
        """ Get catalog tree leaves """
        logging.info(f'Get catalog tree {catalog_id}')
        rq = f'{self.host}/leaf'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        leaves = json.loads(r.text)
        return leaves  

    def getTreeLeaf(self, catalog_id:int, tree_id:int, leaf_id:int, params=None):
        """ Get catalog tree leaf ID """
        logging.info(f'Get catalog tree {catalog_id}')
        rq = f'{self.host}/leaf/{leaf_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        leaf = json.loads(r.text)
        return leaf
    
    #warehouse
    def listWarehouse(self, query=None):
        """
        Read all warehouse
        """
        logging.info('Reading all warehouses')
        rq = f'{self.host}/warehouse'
        agent=self.s.getAgent()
        r = agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        warehouses = json.loads(r.text)
        return warehouses

    def getWarehouse(self, warehouse_id:int, params=None):
        """Get warehouse details"""
        logging.info(f'Get warehouse {warehouse_id}')
        rq = f'{self.host}/warehouse/{warehouse_id}'
        agent=self.s.getAgent()
        r = agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        warehouse = json.loads(r.text)
        return warehouse

    def createWarehouse(self, payload):
        """ 
        Create new warehouse
        """
        logging.info(f'Creating new warehouse {payload}')
        rq = f'{self.host}/warehouse'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        warehouse = json.loads(r.text)
        return warehouse

    def updateWarehouse(self, warehouse_id:int, payload):
        """ 
        Create new warehouse
        """
        logging.info(f'Updateing warehouse {warehouse_id} - {payload}')
        rq = f'{self.host}/warehouse/{warehouse_id}'
        agent=self.s.getAgent()
        r = agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        warehouse = json.loads(r.text)
        return warehouse
    
    def getWarehouseFromName(self, name:str, params=None):
        """read warehouse from name"""
        logging.info(f'Search warehouse from {name}')
        payload ={
            'name' : name
        }
        if params:
            new_payload = dict(item.split("=") for item in params.split('&'))
            payload = {**payload, **new_payload}        
        rq = f'{self.host}/warehouse/findByName'
        agent=self.s.getAgent()
        r = agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)
