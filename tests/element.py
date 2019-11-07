
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
 

def test():
    """ test Element class."""
    # import argparse
    logger.debug('Init test')
    el = Element()
    items = el.getItems('take=2')
    logger.info(items)

if __name__ == '__main__':
    """ Do Test """  
    test()