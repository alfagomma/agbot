
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HOOK test
"""

import logging
from agbot.hook.core import Hook

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
 

def test():
    """ Test Hook class."""
    # import argparse
    logger.debug('Init test')
    h = Hook()
    message = {
        'material_id': 2305278,
        'category':'cls'
    }
    customers = h.erp_sap_material(message)
    logger.info(customers)

if __name__ == '__main__':
    """ Do Test """  
    test()