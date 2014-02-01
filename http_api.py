import sys, getopt
from indico.core import db

from indico.web.http_api.hooks.base import HTTPAPIHook, IteratedDataFetcher
from indico.web.http_api.fossils import IConferenceMetadataFossil, IConferenceMetadataWithSubContribsFossil, \
    IConferenceMetadataWithSessionsFossil
try: from indico.web.http_api.fossils import IConferenceMetadataWithContribsAndBreaksFossil as IContribFossil
except: from indico.web.http_api.fossils import IConferenceMetadataWithContribsFossil as IContribFossil

from indico.web.http_api.util import get_query_parameter
from MaKaC.conference import ConferenceHolder

#from repoze.catalog.catalog import FileStorageCatalogFactory
#from repoze.catalog.catalog import ConnectionManager
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog

from repoze.catalog.query import *

from datetime import datetime
import time
from pytz import timezone
import MaKaC.common.info as info
from MaKaC.plugins.base import PluginsHolder

globalHTTPAPIHooks = ['SearchHook']

@HTTPAPIHook.register
class SearchHook(HTTPAPIHook):
    TYPES = ('conference',)
    RE = r'search'
    DEFAULT_DETAIL = 'events'
    MAX_RECORDS = {
        'events': 1000,
        'contributions': 500,
        'subcontributions': 500,
        'sessions': 100,
    }

    def _getParams(self):
        super(SearchHook, self)._getParams()
        self._start_date = get_query_parameter(self._queryParams, ['start_date'], '1970/01/01')
        self._end_date = get_query_parameter(self._queryParams, ['end_date'], None)
        self._today = get_query_parameter(self._queryParams, ['today'], None)
        self._category = get_query_parameter(self._queryParams, ['category'], None)
        self._keywords = get_query_parameter(self._queryParams, ['keywords'], None)
        # To be implemented...
        self._text = get_query_parameter(self._queryParams, ['text'], None)
        
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
        #plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        #DBpath = plugin.getOptions()["DBpath"].getValue()   
        #factory = FileStorageCatalogFactory(DBpath,'repoze_catalog')
        #manager = ConnectionManager()
        #catalog = factory(manager)
        catalog = RepozeCatalog().catalog
        
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        
        if params._start_date:
            sdate = params._start_date.split('/')
            startDate_ts = timezone(localTimezone).localize(datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]), 0, 0))
        if params._end_date:
            edate = params._end_date.split('/')
            endDate_ts = timezone(localTimezone).localize(datetime(int(edate[0]), int(edate[1]), int(edate[2]), 23, 59))
        else:
            endDate_ts = None
        
        if params._start_date:
            query = InRange('startDate',startDate_ts, endDate_ts)

        if params._today:
            td = params._today.split('/')
            today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 0, 0))
            query = Le('startDate',today_ts) & Ge('endDate',today_ts)            
        
        if params._keywords:
            kw = params._keywords.split(',')
            query = query & Any('keywords', kw)
        
        if params._category:
            kw = params._category.split(',')
            query = query & Any('category', kw)
        
        # Just return Conference objs
        query = query & Eq('collection', 'Conference')
                
        numdocs, results = catalog.query(query)
        results = [catalog.document_map.address_for_docid(result) for result in results]     
        
        res = []
        ch = ConferenceHolder()        
        for obj in results:
            try:
                confId = str(obj).split("|")[0]
                event = ch.getById(confId)
                res.append(event)
            except:
                pass
        return self._process(res)
        
    
    
