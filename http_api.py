import sys, getopt
from indico.core import db

from indico.web.http_api.hooks.base import HTTPAPIHook, IteratedDataFetcher
from indico.web.http_api.fossils import IConferenceMetadataFossil, IConferenceMetadataWithSubContribsFossil, \
    IConferenceMetadataWithSessionsFossil
try: from indico.web.http_api.fossils import IConferenceMetadataWithContribsAndBreaksFossil as IContribFossil
except: from indico.web.http_api.fossils import IConferenceMetadataWithContribsFossil as IContribFossil

from indico.web.http_api.util import get_query_parameter
from repozerQueryManager import RepozerQueryManager

globalHTTPAPIHooks = ['SearchHook']

@HTTPAPIHook.register
class SearchHook(HTTPAPIHook):
    TYPES = ('conference',)
    RE = r'search'
    DEFAULT_DETAIL = 'events'
    MAX_RECORDS = {
        'events': 1000,
        'contributions': 100,
        'subcontributions': 100,
        'sessions': 100,
    }
    NO_CACHE = True

    def _getParams(self):
        super(SearchHook, self)._getParams()
        
        p = {}
        pars = ['id',
                'text',
                'where',
                'start_date',
                'end_date',
                'started',
                'today',
                'todaybeyond',
                'category',
                'keywords',
                'keywordsAnd',
                'limit',
                'desc',
                'valid_deadline'
                ]
        for par in pars:
            val = get_query_parameter(self._queryParams, [par], None)
            if val:
                p[par] = val
        
        self._p = p
        


    def export_conference(self, aw):
        return SearchFetcher(aw, self).searchRepoze(self)

        
class SearchFetcher(IteratedDataFetcher):
    DETAIL_INTERFACES = {
        'events': IConferenceMetadataFossil,
        'contributions': IContribFossil,        
        'subcontributions': IConferenceMetadataWithSubContribsFossil,
        'sessions': IConferenceMetadataWithSessionsFossil
    }
    
        
    def searchRepoze(self, params):
        rqm = RepozerQueryManager(params._p)
        numdocs, res = rqm.getResults()                
        return self._process(res)
        
    
    
