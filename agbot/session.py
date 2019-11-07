
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session
"""

import os, json, time, logging
import requests
import configparser
from redis import Redis
from sys import exit

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# c_handler = logging.StreamHandler()
# c_handler.setLevel(logging.WARNING)
# # Create formatters and add it to handlers
# c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)
# logger.addHandler(c_handler)

class Session(object):
    """
    AGBot Session class .
    """
    agcloud_id = None
    agcloud_key = None
    apibot = None
    ep_agapi = None
    ep_aggraph = None
    ep_aghook = None
    token_name = 'ag:agbot'

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug(f'Init session with {profile_name} profie..')
        ## Config
        config_path = os.path.expanduser('~/.agcloud/config')
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        self.ep_agapi = config.get(profile_name, 'ep_agapi')
        self.ep_aghook = config.get(profile_name, 'ep_aghook')

        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
        if not credentials.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.agcloud_id = credentials.get(profile_name, 'agcloud_id')
        self.agcloud_key = credentials.get(profile_name, 'agcloud_key')

        logger.info('ep_agapi is %s' % self.ep_agapi)
        logger.info('ep_aghook is %s' % self.ep_aghook)  

        redis_host = config.get(profile_name, 'redis_host') if config.has_option(profile_name, 'redis_host') else '127.0.0.1'
        redis_pass = credentials.get(profile_name, 'redis_password') if credentials.has_option(profile_name, 'redis_password') else None

        self.cache = Redis(host=redis_host, password=redis_pass, decode_responses=True)
        self.apibot = requests.Session()
        self.__apibotSession()

    def getToken(self):
        """ Read session token. If not exists, it creates it. """
        logger.debug('Init reading token..')
        token = self.cache.hgetall(self.token_name)
        if not bool(token):
            token = self.__createToken(self.token_name)
        return token

    def __apibotSession(self):
        """Read token session and update apibot headers."""
        logger.debug('Init session boot...')
        token = self.getToken()
        try:
            self.apibot.headers.update({
                'user-agent': 'AGBot-Session',
                'x-uid': token['uid'],
                'x-sid': token['sid'],
                'x-csrf': token['csrf']            
                })
        except Exception:
            logger.error("Fatal error on apibot session", exc_info=True)
        return

    def __createToken(self, token_name):
        """ Create new session token. """
        logger.debug(f'Init new session token {token_name}...')
        rqSid = f'{self.ep_agapi}/session'
        rqCsrf = f'{self.ep_agapi}/session/csrf'
        rqUid = f'{self.ep_agapi}/auth/token'
        rUid = self.apibot.post(rqUid, auth=(self.agcloud_id, self.agcloud_key))
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        responseUid = json.loads(rUid.text)
        tokenExpire = int(time.time()) + responseUid['expires_in']

        uid = responseUid['access_token']
        rSid = self.apibot.post(rqSid)
        if 200 != rSid.status_code:
            parseApiError(rSid)
            return False  
        responseSid = json.loads(rSid.text) 
        sid = responseSid['token']
        rCsrf = self.apibot.post(rqCsrf)
        if 200 != rCsrf.status_code:
                parseApiError(rCsrf)
                return False
        responseCsrf = json.loads(rCsrf.text)
        csrf = responseCsrf['csrfToken']
        agbotsession = {
            'uid' : uid,
            'sid' : sid,
            'csrf' : csrf
        }
        self.cache.hmset(token_name, agbotsession)
        self.cache.expireat(token_name, tokenExpire)
        return agbotsession


def parseApiError(response):
        """ stampa errori api """
        status = response.status_code
        try:
            problem = json.loads(response.text)
        except Exception:
            # Add handlers to the logger
            logger.error('Not jsonable', exc_info=True)
        problem = response.text
        msg = f'status {status}'
        if 'title' in problem:
            msg+=f" / {problem['title']}"
        if 'errors' in problem:
            for k,v in problem['errors'].items():
                msg+=f" -{k}:{v}" 
        logger.warning(msg)
