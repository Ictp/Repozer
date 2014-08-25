import sys, getopt
from indico.core import db

from indico.web.http_api.hooks.base import HTTPAPIHook, IteratedDataFetcher
from indico.web.http_api.fossils import IConferenceMetadataFossil, IConferenceMetadataWithSubContribsFossil, \
    IConferenceMetadataWithSessionsFossil
try: from indico.web.http_api.fossils import IConferenceMetadataWithContribsAndBreaksFossil as IContribFossil
except: from indico.web.http_api.fossils import IConferenceMetadataWithContribsFossil as IContribFossil

from indico.web.http_api.util import get_query_parameter
from MaKaC.conference import ConferenceHolder

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
        'events': 100,
        'contributions': 50,
        'subcontributions': 50,
        'sessions': 100,
    }

    def _getParams(self):
        super(SearchHook, self)._getParams()
        self._id = get_query_parameter(self._queryParams, ['id'], None)
        self._start_date = get_query_parameter(self._queryParams, ['start_date'], '1970/01/01')
        self._end_date = get_query_parameter(self._queryParams, ['end_date'], None)
        self._today = get_query_parameter(self._queryParams, ['today'], None)
        self._todaybeyond = get_query_parameter(self._queryParams, ['todaybeyond'], None)
        self._category = get_query_parameter(self._queryParams, ['category'], None)
        self._keywords = get_query_parameter(self._queryParams, ['keywords'], None)
        self._keywordsAnd = get_query_parameter(self._queryParams, ['keywordsAnd'], None)
        self._limitQuery = get_query_parameter(self._queryParams, ['limit'], None)        
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
        #catalog = RepozeCatalog('repozercatalog_conference').catalog
        catalog = RepozeCatalog().catalog
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        
        confId = None
        
        if params._id:
            confId = params._id
        
        if params._start_date:
            sdate = params._start_date.split('/')
            try:
                startDate_ts = timezone(localTimezone).localize(datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]), 0, 0))
            except:
                return self._process([])
        if params._end_date:
            edate = params._end_date.split('/')
            try:
                endDate_ts = timezone(localTimezone).localize(datetime(int(edate[0]), int(edate[1]), int(edate[2]), 23, 59))
            except:
                return self._process([])
        else:
            endDate_ts = None
        
        if params._start_date:
            #query = InRange('startDate',startDate_ts, endDate_ts)
            query = Not(Lt('endDate',startDate_ts) | Gt('startDate',endDate_ts)) | (InRange('startDate',startDate_ts, endDate_ts))
            # ESCLUDO le conf gia finite e quelle future, AGGIUNGO quelle senza endDate ma con startDate nel range

        if params._today != None:
            if params._today == '':
                td = time.strftime("%Y/%m/%d").split('/')
            else:                
                td = params._today.split('/')
            try:
                #today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 23, 59))
                today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 23, 59))
                end_today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 00, 00))
            except:
                return self._process([])
            query = Le('startDate',today_ts) & Ge('endDate',end_today_ts) 

        
        if params._todaybeyond != None:
            if params._todaybeyond == '':
                td = time.strftime("%Y/%m/%d").split('/')
            else:
                td = params._todaybeyond.split('/')
            try:
                today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 23, 59))
            except:
                return self._process([])
            query = Le('startDate',today_ts) & Ge('endDate',today_ts) | Ge('startDate',today_ts)          
        
        if params._keywords:
            if params._keywords.find(',') > -1:
                kw = params._keywords.split(',')
            else:
                kw = [params._keywords]
            query = query & Any('keywords', kw)
            
        if params._keywordsAnd:
            kw = params._keywordsAnd.split(',')
            query = query & All('keywords', kw)
        
        if params._category:
            kw = params._category.split(',')
            query = query & Any('category', kw)
        
        # Just return Conference objs
        query = query & Eq('collection', 'Conference')
               
               
        #print "QUERY STARTED" 
        res = []
        ch = ConferenceHolder()        

        if confId:
            event = ch.getById(confId)
            res.append(event)
        else:
            if params._limitQuery:
                numdocs, results = catalog.query(query, sort_index='startDate', reverse=True, limit=params._limitQuery)
            else:
                numdocs, results = catalog.query(query, sort_index='startDate', reverse=True)

            #print "QUERY ENDED"    

            results = [catalog.document_map.address_for_docid(result) for result in results]     

            #print "RESULTS MAPPED"
        
            for obj in results:
                try:
                    confId = str(obj).split("|")[0]
                    event = ch.getById(confId)
                    res.append(event)
                except:
                    pass
        
        #print "RETURNING"
        
        return self._process(res)
        
    
    
