
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
 
class testH2o():
    """test h2o"""

    def __init__(self):
        """ init """
        self.h=H2o()

    def customer(self):
        """test customer"""
        customers = self.h.getCustomers('take=5')
        print(customers)


def test():
    """ test H2o class."""
    ts=testH2o()
    ts.customer()

if __name__ == '__main__':
    """ Do Test """  
    test()
