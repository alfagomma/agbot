
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EB2 test
"""

import logging

from agbot.eb2.core import Eb2

class test():
    """test eb2"""

    def __init__(self, profile_name):
        """ init """
        self.e=Eb2(profile_name)

    def company(self):
        """test company"""
        companies = self.e.getCompanies('take=5')
        print(companies)
        company = self.e.getCompany(3)
        print(company)
        ext_id='AG1'
        companyext = self.e.getCompanyFromExt_id(ext_id)
        print(companyext)

def main(args):
    """ start testing """
    logging.basicConfig(level=logging.INFO)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f'Init {__file__}')
    t = test(profile_name=args.profile)
    for atr in args.test:
        if hasattr(t, atr):getattr(t, atr)()
    return
    
def parse_args():
    """Parse the args from main."""
    import argparse
    parser = argparse.ArgumentParser(description='Testing support')
    parser.add_argument("--profile", type=str, help='Use specific profile env')
    parser.add_argument("-t", "--test", nargs='+', help='What can I do for you?', required=True)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)