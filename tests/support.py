
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Support test API
"""

import logging
import time

from agbot.support.core import Support

class test():
    """ test support """

    def __init__(self, profile_name):
        """init"""
        logging.debug(f'Init test {profile_name}')
        self.s = Support(profile_name)

    def category(self):
        """ test category fx."""
        logging.debug('Init test category')
        cat_list = self.s.listCategories('take=3')
        logging.info(cat_list)
        time.sleep(30)
        cat = self.s.readCategory(2, {'include':'type'})
        logging.info(cat)
        return True

    def category_type(self):
        """ test category type fx."""
        logging.debug('Init test category type')
        catype_list = self.s.listCategoryTypes('take=3')
        logging.info(catype_list)
        catype = self.s.readCategory(1, {'include':'type'})
        logging.info(catype)
        return True

    def ticket(self):
        """ test ticket fx."""
        logging.debug('Init test ticket')
        tic_list = self.s.listTicket('take=3')
        logging.info(tic_list)
        return True


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