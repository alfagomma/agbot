
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base test
"""

import logging
from agbot.base.core import Base

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def test():
    """ test Base class."""
    # import argparse
    logger.debug('Init test')
    b = Base()
    uoms = b.getUoms('take=5')
    logger.info(uoms)

if __name__ == '__main__':
    """ Do Test """  
    test()