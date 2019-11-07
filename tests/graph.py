
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Graph test
"""

import logging
from agbot.graph.core import Graph

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
 

def test():
    """ test Graph class."""
    # import argparse
    logger.debug('Init test')
    gn = Graph()
    languages = gn.read_all_language('take=4')
    logger.info(languages)

if __name__ == '__main__':
    """ Do Test """  
    test()