
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
    __agent=False
    __credentials=False
    __cacheKey = 'ag:agbot'

    def __init__(self, profile_name='default'):
        """
        Initialize main class with this and that.
        """
        if not profile_name:
            profile_name = 'default'        
        logger.info(f'Init agbot session with {profile_name} profile.')
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
        #cache
        self.__setCache()

    def __setCache(self):
        """ set cache """
        logger.debug('Setting redis cache...')
        redis_host = self.config.get('redis_host', '127.0.0.1')
        redis_pass = self.__credentials.get('redis_password', None)
        self.cache=Redis(host=redis_host, password=redis_pass, decode_responses=True)
        return True

    def __getToken(self):
        """ Read session token. If not exists, it creates it. """
        logger.info('Init reading token..')
        token = self.cache.hgetall(self.__cacheKey)
        if not token:
            token = self.__createToken()
        return token

    def __setToken(self, payload):
        """save token """
        logger.debug(f'Init set token {payload}')
        expire_in = payload['expires_in']
        uid = payload['access_token']
        token = {
            'uid' : uid
        }
        tokenExpireAt=int(time.time()) + expire_in
        self.cache.hmset(self.__cacheKey, token)
        self.cache.expireat(self.__cacheKey, int(tokenExpireAt))
        return token

    def __createToken(self):
        """ Create new session token. """
        logger.info(f'Init new session token ...')
        agcloud_id = self.__credentials.get('agcloud_id')
        agcloud_key = self.__credentials.get('agcloud_key')
        host = self.config.get('agapi_host')
        rqToken = f'{host}/auth/token'
        rUid = requests.post(rqToken, auth=(agcloud_id, agcloud_key))
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        responseUid = json.loads(rUid.text)
        token = self.__setToken(responseUid)
        return token

    def __refreshToken(self):
        """ Refresh current token. """
        logger.info(f'Init refresh token ...')
        host = self.config.get('agapi_host')
        rq = f'{host}/auth/token'
        rqRefresh = self.__agent.get(rq)
        if 200 != rqRefresh.status_code:
            parseApiError(rqRefresh)
            return False
        responseRefresh = json.loads(rqRefresh.text)
        token = self.__setToken(responseRefresh)
        return token

    def __createSessionAgent(self, token=None):
        """ Create requests session. """
        logger.debug('Creating new requests session')
        agent=requests.Session()
        agent.headers.update({'user-agent': 'AGBot-Session'})
        if not token:
            token = self.__getToken()
            if not token:return False
        try:
            agent.headers.update({'x-uid': token['uid'] })
        except Exception:
            logger.error("Invalid token keys", exc_info=True)
        self.__agent=agent
        return agent

    def getAgent(self):
        """Retrive API request session."""
        logger.info('Get request agent')
        agent=self.__agent
        if not agent:
            agent=self.__createSessionAgent()
        else:
            ttl = self.cache.ttl(self.__cacheKey)
            if ttl < 1:
                agent=self.__createSessionAgent()
            elif 1 <= ttl <= 900:
                refreshedToken=self.__refreshToken()
                agent = self.__createSessionAgent(refreshedToken)
            if not agent:
                logger.error('Unable to create agent!')
                exit(1)
        return agent


def parseApiError(response):
    """ stampa errori api """
    logger.debug('Parsing error')
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
        logger.warning(msg)
    else:
        logger.error(msg)
    return msg
