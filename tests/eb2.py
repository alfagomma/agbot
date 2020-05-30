
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

class testEb2():
    """test eb2"""

    def __init__(self):
        """ init """
        self.e=Eb2()

    def company(self):
        """test company"""
        companies = self.e.getCompanies('take=5')
        print(companies)
        company = self.e.getCompany(3)
        print(company)
        ext_id='AG1'
        companyext = self.e.getCompanyFromExt_id(ext_id)
        print(companyext)

def test():
    """ test Eb2 class."""
    ts=testEb2()
    ts.company() 

if __name__ == '__main__':
    """ Do Test """  
    test()
