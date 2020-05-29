
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session
"""

import configparser
import json
import logging
import os
import time
from sys import exit

import requests
from redis import Redis

logger = logging.getLogger(__name__)

class Session(object):
    """
    AGBot Session class .
    """
    
    config=False
    __credentials=False
    __tokenName = 'ag:agbot'

    def __init__(self, profile_name='default'):
        """
        Initialize main class with this and that.
        """
        if not profile_name:
            profile_name = 'default'        
        logger.info(f'Init agbot session with {profile_name} profie..')
        ## Config
        config_path = os.path.expanduser('~/.agcloud/config')
        cp = configparser.ConfigParser()
        cp.read(config_path)
        if not cp.has_section(profile_name):
            logger.error(f'Unknow {profile_name} configs!')
            exit(1)
        self.config=cp[profile_name]
        # #hosts
        ## Credentials
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        ccp = configparser.ConfigParser()
        ccp.read(credentials_path)
        if not ccp.has_section(profile_name):
            logger.error(f'Unknow {profile_name} credentials!')
            exit(1)
        self.__credentials=ccp[profile_name]
        # #cache
        self.__setCache()

    def __setCache(self):
        """ set cache """
        logger.debug('Setting redis cache...')
        redis_host = self.config.get('redis_host', '127.0.0.1')
        redis_pass = self.__credentials.get('redis_password', None)
        cache=Redis(host=redis_host, password=redis_pass, decode_responses=True)
        self.cache=cache
        return True

    def __getToken(self, rq):
        """ Read session token. If not exists, it creates it. """
        logger.info('Init reading token..')
        token = self.cache.hgetall(self.__tokenName)
        if not token:
            token = self.__createToken(rq)
        return token

    def __createToken(self, rq):
        """ Create new session token. """
        logger.info(f'Init new session token ...')
        agcloud_id = self.__credentials.get('agcloud_id')
        agcloud_key = self.__credentials.get('agcloud_key')
        host = self.config.get('agapi_host')
        rqSession = f'{host}/session'
        rqCsrf = f'{host}/session/csrf'
        rqToken = f'{host}/auth/token'
        rUid = rq.post(rqToken, auth=(agcloud_id, agcloud_key))
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        responseUid = json.loads(rUid.text)
        tokenExpire = int(time.time()) + responseUid['expires_in']

        uid = responseUid['access_token']
        rSid = rq.post(rqSession)
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
        csrf = responseCsrf['csrf_token']
        token = {
            'uid' : uid,
            'sid' : sid,
            'csrf' : csrf
        }
        self.cache.hmset(self.__tokenName, token)
        self.cache.expireat(self.__tokenName, tokenExpire)
        return token

    def createAgent(self, auth=True):
        """Create a new request session."""
        logger.info(f'Creating new request session {auth}...')
        s = requests.Session()
        s.headers.update({'user-agent': 'AGBot-Session'})
        if not auth:
            logger.debug('Session without auth')
            return s
        # Auth agent
        token = self.__getToken(s)
        if not token:
            return False
        try:
            s.headers.update({
                'x-uid': token['uid'],
                'x-sid': token['sid'],
                'x-csrf': token['csrf']
                })
        except Exception:
            logger.error("Invalid token keys", exc_info=True)
        return s


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
    if status >=400 and status <500:
        logger.debug(msg)
    else:
        logger.warning(msg)
    return msg
