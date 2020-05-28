
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
H2O test
"""

import logging
from agbot.h2o.core import H2o

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
 

def test():
    """ test H2o class."""
    # import argparse
    logger.debug('Init test')
    h = H2o()
    customers = h.getCustomers('take=5')
    logger.info(customers)
    ordertypes=h.getOrderTypeFromName('bill')
    logger.info(ordertypes)

if __name__ == '__main__':
    """ Do Test """  
    test()