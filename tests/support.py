
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support test API
"""

import logging
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
        logger.info(cat_list)
        cat = self.s.readCategory(1, {'include':'type'})
        logger.info(cat)

    def categoryType(self):
        """ test category type fx."""
        logger.debug('Init test category type')
        catype_list = self.s.listCategoryTypes('take=3')
        logger.info(catype_list)
        catype = self.s.readCategory(1, {'include':'type'})
        logger.info(catype)

    def ticket(self):
        """ test ticket fx."""
        logger.debug('Init test ticket')
        tic_list = self.s.listCategoryTypes('take=3')
        logger.info(tic_list)
        tick = self.s.readCategory(1, {'include':'type'})
        logger.info(tick)        


def test():
    ts=testSupport()
    ts.category()
    ts.categoryType()
    ts.ticket()

if __name__ == '__main__':
    """ Do Test """  
    test()