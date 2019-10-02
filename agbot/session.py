
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Session
"""

import os
import requests
import json
import time
import logging
import redis
import configparser
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
    Element core class .
    """

    def __init__(self, profile_name=None):
        """
        Initialize main class with this and that.
        """
        logger.debug('Ciao inizializzo session ....')
        config_path = os.path.expanduser('~/.agcloud/config')
        credentials_path = os.path.expanduser('~/.agcloud/credentials')
        config = configparser.ConfigParser()
        config.read(config_path)
        credentials = configparser.ConfigParser()
        credentials.read(credentials_path)
 
        if profile_name is not None:
            print('Reading profile %s' % profile_name)
            if not config.has_section(profile_name):
                logger.error('Questo profilo configurazioni non esiste')
                exit(1)
            if not credentials.has_section(profile_name):
                logger.error('Questo profilo credenziali non esiste')
                exit(1)            
        else:
            profile_name = 'default'
        logger.debug('profile_name is %s' % profile_name)
        self.agcloud_id = credentials.get(profile_name, 'agcloud_id')
        self.agcloud_key = credentials.get(profile_name, 'agcloud_key')
        self.ep_auth = config.get(profile_name, 'ep_auth')
        logger.debug('ep_auth is %s' % self.ep_auth)
        self.ep_agcloud = config.get(profile_name, 'ep_agcloud')
        logger.debug('ep_agcloud is %s' % self.ep_agcloud)        
        self.ep_h2o = config.get(profile_name, 'ep_h2o')
        logger.debug('ep_h2o is %s' % self.ep_h2o)
        self.ep_element = config.get(profile_name, 'ep_element')
        logger.debug('ep_element is %s' % self.ep_element)
        self.ep_sqm = config.get(profile_name, 'ep_sqm')
        logger.debug('ep_sqm is %s' % self.ep_sqm)   
        self.ep_eb2 = config.get(profile_name, 'ep_eb2')
        logger.debug('ep_eb2 is %s' % self.ep_eb2)
        self.ep_hook = config.get(profile_name, 'ep_hook')
        logger.debug('ep_hook is %s' % self.ep_hook)                     
        self.redis_host = config.get(profile_name, 'redis_host') if config.has_option(profile_name, 'redis_host') else '127.0.0.1'
        self.redis_pass = config.get(profile_name, 'redis_pass') if config.has_option(profile_name, 'redis_pass') else None
        self.cache = redis.Redis(host=self.redis_host, password=self.redis_pass, decode_responses=True)
        self.apibot = requests.Session()
        self.sessione()
 
    def sessione(self):
        """prende sessione"""
        logger.debug('Init sessione')
        token = self.getToken()
        self.apibot.headers.update({
            'user-agent': 'AGBot-Session',
            'x-uid': token['uid'],
            'x-sid': token['sid'],
            'x-csrf': token['csrf']            
            })        

    def getToken(self):
        """ Prende token di sessione utente """
        logger.debug('Init getToken')
        token_name = 'ag:agbot'
        token = self.cache.hgetall(token_name)
        if not bool(token):
            logger.info('Creo nuova sessione')
            token = self.createToken(token_name)
        return token

    def createToken(self, token_name):
        """ Crea token di sessione """
        logger.debug(f'Creo un nuovo session token {token_name}')
        rqSid = '%s/session' % self.ep_auth
        rqCsrf = '%s/session/csrf' % self.ep_auth
        rqUid = '%s/auth/token' % self.ep_auth
        rUid = self.apibot.post(rqUid, auth=(self.agcloud_id, self.agcloud_key))
        if 200 != rUid.status_code:
            parseApiError(rUid)
            return False
        responseUid = json.loads(rUid.text)
        expirein = int(time.time()) + responseUid['expires_in']

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
        self.cache.expireat(token_name, expirein)
        return agbotsession


def parseApiError(response):
        """ stampa errori api """
        status = response.status_code
        try:
            problem = json.loads(response.text)
        except Exception:
            # Add handlers to the logger
            logger.error('Not jsonable')
            problem = response.text
        msg = f'status {status}'
        if 'title' in problem:
            msg+=f" / {problem['title']}"
        if 'errors' in problem:
            for k,v in problem['errors'].items():
                msg+=f" -{k}:{v}" 
        logger.warning(msg)
