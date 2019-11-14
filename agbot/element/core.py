
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Element SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.1"
__date__ = "2019-11-04"

import json, logging, time
from agbot.session import Session, parseApiError

logger = logging.getLogger()
class Element(object):
    """
    Element core class .
    """

    def __init__(self, profile_name='default'):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Element SDK')
        session = Session(profile_name)
        self.agent = session.create()
        self.host = session.getAgapiHost()

    #item
    def getItem(self, item_id:int, params=None):
        """
        Legge un item dal suo id.
        """
        logger.debug(f'Get item {item_id}')
        rq = f'{self.host}/item/{item_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        item = json.loads(r.text)
        return item

    def getItems(self, query=None):
        """
        Prende tutti gli items.
        """
        logger.debug('Getting all the items')
        rq = '%s/item' % (self.host)
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        _items = json.loads(r.text)
        return _items

    def createItem(self, payload):
        """
        Create new item.
        """
        logger.debug('Creating item %s' % payload)
        rq = '%s/item' % (self.host)
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/item/findByExtId' % (self.host)
        r = self.agent.get(rq, params=payload)
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
        rq = '%s/item/findByCode' % (self.host)
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def getItemFromErpId(self, erp_id:int, ext_id:str):
        """
        Get item from ext_id of Erp.
        """
        logger.debug(f'Search item ext_id {ext_id} for erp {erp_id}.')
        rq = '%s/item/findByErpExtId' % (self.host)
        payload = {
            'erp_id' : erp_id,
            'ext_id' : ext_id
        }
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    def updateItem(self, item_id:int, payload):
        """
        Update item.
        """
        logger.debug(f'Updating item {item_id} with {payload}')
        rq = '%s/item/%s' % (self.host, item_id)
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def patchItem(self, item_id:int, payload):
        """
        Patch know item field.
        """
        logger.debug(f'Patching item {item_id} with {payload}')
        rq = '%s/item/%s' % (self.host, item_id)
        r = self.agent.patch(rq, json=payload)
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
        rq = '%s/item/%s/attribute' % (self.host, item_id)
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)

    def syncItemNorm(self, item_id:int, payload):
        """
        Sync item norm.
        """
        logger.debug(f'Sync item {item_id} norm {payload}')
        rq = '%s/item/%s/norm' % (self.host, item_id)
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/item/%s/catalog/sync' % (self.host, item_id)
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/item/%s/cad' % (self.host, item_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        try:
            r = self.agent.post(rq, files=files)
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
        rq = f'{self.host}/item/{item_id}/cad/{cad_id}'
        try:
            r = self.agent.delete(rq)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    #attribute
    def createAttribute(self, payload):
        """ crea un nuovo attributo """
        logger.debug('Creating new attribute %s' % payload)
        rq = '%s/attribute' % (self.host)
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        attribute = json.loads(r.text)
        logger.info('Create attribute %s' % attribute['data']['id'])
        return attribute

    def getAttributeByName(self, attribute_name:str, params=None):
        """ Attribute by name """
        payload ={
            'name' : attribute_name
        }
        if params:
            new_payload = dict(item.split("=") for item in params.split('&'))
            payload = {**payload, **new_payload}
        logger.debug('Get attribute %s' % attribute_name)
        rq = '%s/attribute/findByName' % (self.host)
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 

    #family
    def createFamily(self, payload):
        """ crea una nuova famiglia """
        logger.debug('Creating new family %s' % payload)
        rq = '%s/family' % (self.host)
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/family' % (self.host)
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        families = json.loads(r.text)
        return families

    def getFamily(self, family_id:int, params=None):
        """
        Legge la singola famiglia.
        """
        logger.debug(f'Reading family {family_id}')
        rq = '%s/family/%s' % (self.host, family_id)
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        _family = json.loads(r.text)
        return _family

    def updateFamily(self, family_id:int, payload):
        """
        Update family.
        """
        logger.debug('Updating family %s ...' % family_id)
        rq = '%s/family/%s' % (self.host, family_id)
        r = self.agent.post(rq, json=payload) 
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
        rq = '%s/family/findByCode' % (self.host)
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)    

    def patchFamily(self, family_id:int, payload):
        """
        Associa categoria a famiglia
        """
        logger.debug(f'Patching family {family_id} ')
        rq = '%s/family/%s' % (self.host, family_id)
        try:
            r = self.agent.patch(rq, json=payload)
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
        logger.debug(f'Patching family {family_id} with category {category_id}')
        rq = '%s/family/%s' % (self.host, family_id)
        payload = {
            'category_id': category_id
            }
        try:
            r = self.agent.patch(rq, json=payload)
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
        rq = '%s/family/%s' % (self.host, family_id)
        payload = {
            'datasheet_id': datasheet_id
            }
        try:
            r = self.agent.patch(rq, json=payload)
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
        rq = '%s/family/%s/cover' % (self.host, family_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        #files = {'src': ('test.cad', open(filepath, 'rb'), 'image/png')}
        try:
            r = self.agent.post(rq, files=files)
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
        rq = '%s/family/%s/hq' % (self.host, family_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        #files = {'src': ('test.cad', open(filepath, 'rb'), 'image/png')}
        try:
            r = self.agent.post(rq, files=files)
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
        rq = '%s/family/%s/norm' % (self.host, family_id)
        payload = {
            'norm_id' : norm_id
            }
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/family/%s/quality' % (self.host, family_id)
        payload = {
            'quality_id' : quality_id
            }
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/family/%s/feature' % (self.host, family_id)
        try:
            r = self.agent.post(rq, json=payload)
        except Exception:
            logger.exception('Exception occured')
            return False
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def attachFamilyAttribute(self, family_id:int, attribute_id:int):
        """
        Add attribute to family.
        """
        logger.debug(f'Attaching attribute {attribute_id} to family {family_id}...')
        rq = f'{self.host}/family/{family_id}/attribute'
        payload = {
            'attribute_id' : attribute_id
            }
        r = self.agent.post(rq, json=payload)
        if 204 != r.status_code:
            parseApiError(r)
            return False
        return True

    def attachFamilySorting(self, family_id:int, attribute_id:int):
        """
        Add attribute to sorting
        """
        logger.debug(f'Attaching attribute {attribute_id} to family {family_id} sorting...')
        rq = f'{self.host}/family/{family_id}/sorting'
        payload = {
            'attribute_id' : attribute_id
            }
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/feature' % (self.host)
        payload = {
            'name' : feature_name
            }
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/feature/findByName' % (self.host)
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _features = json.loads(r.text)
        return _features

    #crtable
    def createCrtable(self, payload):
        """ crea una nuova tabella """
        logger.debug('Creating new crtabel %s' % payload)
        rq = '%s/crtable' % (self.host)
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        crtable = json.loads(r.text)
        logger.info('Create crtable %s' % crtable['data']['id'])
        return crtable

    def getCrtable(self, crtable_id:int, params=None):
        """
        Legge una tabella dal suo id.
        """
        logger.debug(f'Get crtable {crtable_id}')
        rq = f'{self.host}/crtable/{crtable_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable

    def getCrtableFromSlug(self, slug:str):
        """
        Legge una tabella dal suo slug.
        """
        logger.debug(f'Get crtable slug {slug}')
        rq = f'{self.host}/crtable/findBySlug'
        r = self.agent.get(rq, params={
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
        logger.debug(f'Get crtable name {name}')
        rq = f'{self.host}/crtable/findByName'
        r = self.agent.get(rq, params={
            'name' : name
        })
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable


    #crimping
    def createCrimping(self, crtable_id:int, payload):
        """ crea nuovo parametro di pinzatura per tabella """
        logger.debug('Creating new crimping %s' % payload)
        rq = f'{self.host}/crtable/{crtable_id}/crimping'
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        crimping = json.loads(r.text)
        logger.info('Create crimping %s' % crimping['data']['id'])
        return crimping

    def getCrimping(self, crtable_id:int, crimping_id:int, params=None):
        """
        Legge un parametro dalla tabella pinzatura.
        """
        logger.debug(f'Get crimping {crimping_id} from table {crtable_id}')
        rq = f'{self.host}/crtable/{crtable_id}/crimping/{crimping_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        crtable = json.loads(r.text)
        return crtable

    #hub
    def getHubByName(self, hub_name:str):
        """ 
        Get hub from name
        """
        logger.debug('Search hub by name %s' % hub_name)
        rq = f'{self.host}/hub/findByName?name={hub_name}'
        r = self.agent.get(rq)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _hub = json.loads(r.text)
        return _hub

    def createHub(self, hub_name:str):
        """ 
        Create new hub
        """
        logger.debug('Creating new hub with name %s' % hub_name)
        rq = f'{self.host}/hub'
        payload = {'name':hub_name}
        r = self.agent.post(rq, json=payload)
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
        logger.debug('Creating new category with name %s at hub %s' % (category_name, hub_id))
        rq = '%s/category' % (self.host)
        payload = {
            'hub_id': hub_id,
            'name':category_name
            }
        r = self.agent.post(rq, json=payload)
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
        rq = '%s/category/findByName?name=%s' % (self.host, category_name)
        r = self.agent.get(rq)
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
        rq = '%s/category/%s/cover' % (self.host, category_id)
        fin = open(localFile, 'rb')
        files = {'src': fin}
        try:
            r = self.agent.post(rq, files=files)
        except Exception:
            logging.exception("Exception occurred")
            return False
        if 200 != r.status_code:
            parseApiError(r)
            return False
        _category = json.loads(r.text)        
        return _category

    #catalog
    def getCatalog(self, catalog_id:int, params=None):
        """ Get catalog by ID """
        logger.debug(f'Get catalog {catalog_id}')
        rq = f'{self.host}/catalog/{catalog_id}'
        logger.debug(rq)
        r = self.agent.get(rq, params=params)
        logger.debug(r)
        if 200 != r.status_code:
            return False
        item = json.loads(r.text)
        return item

    def getTree(self, catalog_id:int, tree_id:int, params=None):
        """ Get catalog tree by ID """
        logger.debug(f'Get catalog tree {catalog_id}')
        rq = f'{self.host}/catalog/{catalog_id}/tree/{tree_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        tree = json.loads(r.text)
        return tree    

    def getTreeLeaves(self, catalog_id:int, tree_id:int, params=None):
        """ Get catalog tree leaves """
        logger.debug(f'Get catalog tree {catalog_id}')
        rq = f'{self.host}/leaf'
        params = {
            'tree': tree_id
        }
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        leaves = json.loads(r.text)
        return leaves  

    def getTreeLeaf(self, catalog_id:int, tree_id:int, leaf_id:int, params=None):
        """ Get catalog tree leaf ID """
        logger.debug(f'Get catalog tree {catalog_id}')
        rq = f'{self.host}/leaf/{leaf_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        leaf = json.loads(r.text)
        return leaf       