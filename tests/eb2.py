
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EB2 test
"""

import logging
from agbot.eb2.core import Eb2

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
 

def test():
    """ test Eb2 class."""
    # import argparse
    logger.debug('Init test')
    h = Eb2()
    companies = h.getCompanies('take=5')
    logger.info(companies)
    # company by id
    idc=4
    company = h.getCompany(idc)
    logger.info(company)
    # company by ext_id
    ext_id='AG1'
    company = h.getCompanyFromExt_id(ext_id)
    logger.info(company)    

if __name__ == '__main__':
    """ Do Test """  
    test()