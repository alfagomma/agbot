
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GRAPH SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.1"
__date__ = "2019-11-07"

import json
import logging
import time

from agbot.session import Session, parseApiError

class Graph(object):
    """
    Graph Open Data core class .
    """
    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logging.debug('Init Graph SDK')
        s = Session(profile_name)
        rqagent =  s.createAgent()
        if not rqagent:
            logging.error('Unable to start base core without valid session.')
            exit(1)
        host=s.config.get('aggraph_host')
        self.host = host
        self.agent = rqagent

    def get_language(self, language_id:int, params=None):
        """
        Read single language
        """
        logging.debug(f'Get language {language_id}')
        rq = f'{self.host}/language/{language_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        language = json.loads(r.text)
        return language

    def read_all_language(self, query=None):
        """
        Read all public languages.
        """
        logging.debug('Getting all the languages')
        rq = '%s/language' % (self.host)
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        languages = json.loads(r.text)
        return languages        
