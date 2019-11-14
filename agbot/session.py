
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session
"""

import os, json, time, logging, requests, configparser
from sys import exit

logger = logging.getLogger()

class Session(object):
    """
    AGBot Session class .
    """
    tokenName = 'ag:agbot'

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        if not profile_name:
            profile_name = 'default'        
        logger.info(f'Init session with {profile_name} profie..')
        ## Config
        config_path = os.path.expanduser('~/.agcloud/config')
        config = configparser.ConfigParser()
        config.read(config_path)
        if not config.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
        if not credentials.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.profile = profile_name
        self.config = config
        self.credentials = credentials
        self.cache = self.__getCache()
        

    def create(self, auth=True):
        """Create a new request session."""
        logger.info(f'Creating new request session {auth}...')
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

    def getAgapiHost(self):
        """ return ag api host"""
        logger.debug('Reading ag api host...')
        agapiHost = self.config.get(profile_name, 'agapi_host')
        return agapiHost

    def getGraphHost(self):
        """ return ag graph host"""
        logger.debug('Reading ag graph host...')
        graphHost = self.config.get(profile_name, 'aggraph_host')
        return graphHost

    def getHookHost(self):
        """ return ag hook host"""
        logger.debug('Reading ag hook host...')
        hookHost = self.config.get(profile_name, 'aghook_host')
        return hookHost        

    def __getToken(self, rq):
        """ Read session token. If not exists, it creates it. """
        logger.info('Init reading token..')
        token = self.cache.hgetall(self.tokenName)
        if not bool(token):
            token = self.__createToken(rq)
        return token

    def __createToken(self, rq):
        """ Create new session token. """
        logger.info(f'Init new session token ...')
        agcloud_id = self.credentials.get(self.profile, 'agcloud_id')
        agcloud_key = self.credentials.get(self.profile, 'agcloud_key')
        host = self.agapi_host()
        rqSid = f'{host}/session'
        rqCsrf = f'{host}/session/csrf'
        rqUid = f'{host}/auth/token'
        rUid = rq.post(rqUid, auth=(agcloud_id, agcloud_key))
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
        token = {
            'uid' : uid,
            'sid' : sid,
            'csrf' : csrf
        }
        self.cache.hmset(self.tokenName, token)
        self.cache.expireat(self.tokenName, tokenExpire)
        return token

    def __getCache(self):
        """cache """
        logger.info('Creating cache...')
        from redis import Redis
        redis_host = self.config.get(self.profile, 'redis_host') if self.config.has_option(self.profile, 'redis_host') else '127.0.0.1'
        redis_pass = self.credentials.get(self.profile, 'redis_password') if self.credentials.has_option(self.profile, 'redis_password') else None
        cache = Redis(host=redis_host, password=redis_pass, decode_responses=True)
        return cache

def parseApiError(response):
        """ stampa errori api """
        status = response.status_code
        try:
            problem = json.loads(response.text)
        except Exception:
            # Add handlers to the logger
            logger.error('Not jsonable', exc_info=True)
            return False
        msg = f'status {status}'
        if 'title' in problem:
            msg+=f" / {problem['title']}"
        if 'errors' in problem:
            for k,v in problem['errors'].items():
                msg+=f'\n\t -{k}:{v}'
        logger.warning(msg)
