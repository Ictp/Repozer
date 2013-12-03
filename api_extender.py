##############################
# Repozer Search EXPORT Hook #
##############################

import sys, getopt
from MaKaC.common import db

from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
from repoze.catalog.query import *

from datetime import datetime
import time
from pytz import timezone
import MaKaC.common.info as info
from MaKaC.plugins.base import PluginsHolder


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
        self._category = get_query_parameter(self._queryParams, ['category'], None)
        self._keywords = get_query_parameter(self._queryParams, ['keywords'], None)
        self._text = get_query_parameter(self._queryParams, ['text'], None)
        
    def export_conference(self, aw):
        
        return SearchFetcher(aw, self).searchRepoze(self)

        
class SearchFetcher(IteratedDataFetcher):
    DETAIL_INTERFACES = {
        'events': IConferenceMetadataFossil,
        'contributions': IConferenceMetadataWithContribsFossil,
        'subcontributions': IConferenceMetadataWithSubContribsFossil,
        'sessions': IConferenceMetadataWithSessionsFossil
    }
        
    
        
    def searchRepoze(self, params):
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        DBpath = plugin.getOptions()["DBpath"].getValue()   
        factory = FileStorageCatalogFactory(DBpath,'indico_catalog')
        manager = ConnectionManager()
        catalog = factory(manager)
        
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        
        sdate = params._start_date.split('/')
        startDate_ts = timezone(localTimezone).localize(datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]), 0, 0))
        if params._end_date:
            edate = params._end_date.split('/')
            endDate_ts = timezone(localTimezone).localize(datetime(int(edate[0]), int(edate[1]), int(edate[2]), 23, 59))
        else:
            endDate_ts = None
        
        query = InRange('startDate',startDate_ts, endDate_ts)
        
        if params._keywords:
            kw = params._keywords.split(',')
            query = query & Any('keywords', kw)
        
        if params._category:
            kw = params._category.split(',')
            query = query & Any('category', kw)
        
        numdocs, results = catalog.query(query)
        
        res = []
        ch = ConferenceHolder()
        
        for obj in results:
            confId = str(obj)
            if obj > 99990: # this is only for ICTP migrated conferences
                confId = 'a'+str(obj)[4:]    
            event = ch.getById(confId)
            res.append(event)
        return self._process(res)
    
    
    
###### /Repozer  