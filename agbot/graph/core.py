
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GRAPH SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "2.1.1"
__date__ = "2019-11-07"

import json, logging, time
from agbot.session import Session, parseApiError

logger = logging.getLogger()
class Graph(object):
    """
    Graph Open Data core class .
    """
    def __init__(self, profile_name='default'):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Graph SDK')
        session = Session(profile_name)
        self.agent = session.create(False)
        self.host = session.aggraph_host

    def get_language(self, language_id:int, params=None):
        """
        Read single language
        """
        logger.debug(f'Get language {language_id}')
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
        logger.debug('Getting all the languages')
        rq = '%s/language' % (self.host)
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        languages = json.loads(r.text)
        return languages        