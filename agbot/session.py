
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
    agapi_host = None
    aggraph_host = None
    aghook_host = None
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
        self.agapi_host = config.get(profile_name, 'agapi_host')
        self.aghook_host = config.get(profile_name, 'aghook_host')
        self.aggraph_host = config.get(profile_name, 'aggraph_host')

        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
        if not credentials.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.agcloud_id = credentials.get(profile_name, 'agcloud_id')
        self.agcloud_key = credentials.get(profile_name, 'agcloud_key')
        redis_host = config.get(profile_name, 'redis_host') if config.has_option(profile_name, 'redis_host') else '127.0.0.1'
        redis_pass = credentials.get(profile_name, 'redis_password') if credentials.has_option(profile_name, 'redis_password') else None
        self.cache = Redis(host=redis_host, password=redis_pass, decode_responses=True)
        logger.info('agapi_host is %s' % self.agapi_host)
        logger.info('aghook_host is %s' % self.aghook_host)  

    def create(self, auth=True):
        """Create a new request session."""
        logger.debug(f'Creating new request session {auth}...')
        rq = requests.Session()
        rq.headers.update({'user-agent': 'AGBot-Session'})
        if not auth:
            logger.debug('Session without auth')
            return rq
        # Auth agent
        token = self.__getToken(rq)
        try:
            rq.headers.update({
                'x-uid': token['uid'],
                'x-sid': token['sid'],
                'x-csrf': token['csrf']
                })
        except Exception:
            logger.error("Fatal error on apibot session", exc_info=True)
        return rq

    def __getToken(self, rq):
        """ Read session token. If not exists, it creates it. """
        logger.debug('Init reading token..')
        token = self.cache.hgetall(self.token_name)
        if not bool(token):
            token = self.__createToken(rq)
        return token

    def __createToken(self, rq):
        """ Create new session token. """
        logger.debug(f'Init new session token {self.token_name}...')
        rqSid = f'{self.agapi_host}/session'
        rqCsrf = f'{self.agapi_host}/session/csrf'
        rqUid = f'{self.agapi_host}/auth/token'
        rUid = rq.post(rqUid, auth=(self.agcloud_id, self.agcloud_key))
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        responseUid = json.loads(rUid.text)
        tokenExpire = int(time.time()) + responseUid['expires_in']

        uid = responseUid['access_token']
        rSid = rq.post(rqSid)
        if 200 != rSid.status_code:
            parseApiError(rSid)
            return False  
        responseSid = json.loads(rSid.text) 
        sid = responseSid['token']
        rCsrf = rq.post(rqCsrf)
        if 200 != rCsrf.status_code:
            parseApiError(rCsrf)
            return False
        responseCsrf = json.loads(rCsrf.text)
        csrf = responseCsrf['csrfToken']
        agentSession = {
            'uid' : uid,
            'sid' : sid,
            'csrf' : csrf
        }
        self.cache.hmset(self.token_name, agentSession)
        self.cache.expireat(self.token_name, tokenExpire)
        return agentSession

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
