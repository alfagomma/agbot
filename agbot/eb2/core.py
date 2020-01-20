
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Eb2 SDK
"""

__author__ = "Davide Pellegrino"
__version__ = "1.1.2"
__date__ = "2020-01-20"

import json, logging, time
from agbot.session import Session, parseApiError

logger = logging.getLogger()
class Eb2(object):
    """
    Eb2 core class .
    """

    def __init__(self, profile_name=False):
        """
        Initialize main class with this and that.
        """
        logger.debug('Init Eb2 SDK')
        session = Session(profile_name)
        rqagent =  session.create()
        if not rqagent:
            logger.error('Unable to start eb2 core without valid session.')
            exit(1)
        self.agent = rqagent
        self.host = f'{session.getAgapiHost()}/eb2'

    #company
    def getCompany(self, company_id:int, params=None):
        """
        Legge un company dal suo id.
        """
        logger.debug(f'Get company {company_id}')
        rq = f'{self.host}/company/{company_id}'
        r = self.agent.get(rq, params=params)
        if 200 != r.status_code:
            return False
        company = json.loads(r.text)
        return company

    def getCompanies(self, query=None):
        """
        Prende tutti gli companies.
        """
        logger.debug('Getting all the companies')
        rq = '%s/company' % (self.host)
        r = self.agent.get(rq, params=query)
        if 200 != r.status_code:
            return False
        _companies = json.loads(r.text)
        return _companies

    def createCompany(self, payload):
        """
        Create new company.
        """
        logger.debug('Creating company %s' % payload)
        rq = '%s/company' % (self.host)
        r = self.agent.post(rq, json=payload)
        if 201 != r.status_code:
            parseApiError(r)
            return False
        company = json.loads(r.text)
        logger.info('Create company %s' % company['data']['id'])
        return company

    def getCompanyFromExt_id(self, ext_id:int, params=None):
        """
        Get company from ext_id.
        """
        logger.debug(f'Search company ext_id {ext_id}.')
        payload ={
            'ext_id' : ext_id
        }
        if params:
            new_payload = dict(company.split("=") for company in params.split('&'))
            payload = {**payload, **new_payload}        
        rq = '%s/company/findByExtId' % (self.host)
        r = self.agent.get(rq, params=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text) 
 
    def updateCompany(self, company_id:int, payload):
        """
        Update company.
        """
        logger.debug(f'Updating company {company_id} with {payload}')
        rq = '%s/company/%s' % (self.host, company_id)
        r = self.agent.post(rq, json=payload)
        if 200 != r.status_code:
            parseApiError(r)
            return False
        return json.loads(r.text)
