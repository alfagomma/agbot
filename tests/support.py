
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support test API
"""

import logging
import time
from agbot.support.core import Support

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class testSupport():
    """ test support """

    def __init__(self):
        """init"""
        self.s = Support()

    def category(self):
        """ test category fx."""
        logger.debug('Init test category')
        cat_list = self.s.listCategories('take=3')
        print(cat_list)
        print('------------------------------------------')
        time.sleep(30)
        cat = self.s.readCategory(2, {'include':'type'})
        print(cat)

    def categoryType(self):
        """ test category type fx."""
        logger.debug('Init test category type')
        catype_list = self.s.listCategoryTypes('take=3')
        print(catype_list)
        catype = self.s.readCategory(1, {'include':'type'})
        print(catype)

    def ticket(self):
        """ test ticket fx."""
        logger.debug('Init test ticket')
        tic_list = self.s.listCategoryTypes('take=3')
        print(tic_list)
        tick = self.s.readCategory(1, {'include':'type'})
        print(tick)        


def test():
    ts=testSupport()
    ts.category()
    # ts.categoryType()
    # ts.ticket()

if __name__ == '__main__':
    """ Do Test """  
    test()