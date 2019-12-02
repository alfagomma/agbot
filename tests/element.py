
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Element test
"""

import logging
from agbot.element.core import Element

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

el = Element()

def itemWarehouse():
    """ test item warehouse"""
    item_id=9865
    newWH={
        'warehouse_id':29,
        'available':29,
        'available_60':10
    }
    el.itemAddWarehouse(item_id, newWH)
    #patch
    whid=6
    patchWH = {
        'available': 156,
        'available_60': 12
    }
    el.itemPatchWarehouse(item_id, whid, patchWH)
    #remove
    whid=6
    el.itemRemoveWarehouse(item_id, whid)


def testwh():
    """ test Element class."""
    # import argparse
    logger.debug('Init test')
    payload={
        'name': 'test_agbot',
        'description': "description test agbot"
    }
    create_wh = el.createWarehouse(payload)
    logger.info(create_wh)
    if create_wh:
        wh_id = create_wh['data']['id']
        get_wh=el.getWarehouse(wh_id)
        logger.info(get_wh)

def test():
    """ test Element class."""
    # import argparse
    logger.debug('Init test')
    items = el.getItems('take=2')
    logger.info(items)
    findfrom=el.getItemFromExt_id(2012771)
    logger.info(findfrom)

if __name__ == '__main__':
    """ Do Test """  
    itemWarehouse()