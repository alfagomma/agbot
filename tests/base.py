
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

class testBase():
    """ Test base """

    def __init__(self):
        """init"""
        self.b = Base()

    def uom(self):
        """unit of measure tests."""
        logger.debug('Init test category')
        uoms = self.b.getUoms('take=5')
        print(uoms)

def test():
    """ test Base class."""
    ts=testBase()
    ts.uom()
    
if __name__ == '__main__':
    """ Do Test """  
    test()
