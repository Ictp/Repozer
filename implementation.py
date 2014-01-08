# -*- coding: utf-8 -*-
##
##
## This file is part of Indico.
## Copyright (C) 2002 - 2013 European Organization for Nuclear Research (CERN).
##
## Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico;if not, see <http://www.gnu.org/licenses/>.
from flask import session

import os, re, datetime, cgi, time, copy
from indico.ext.search.base.implementation import SearchEngineCallAPIAdapter, Author, SearchResult, SubContributionEntry, ContributionEntry, ConferenceEntry, SEATranslator
import indico.ext.search.repozer
import MaKaC.conference as conference
from indico.core.config import Config
from MaKaC.common.output import XSLTransformer
from MaKaC.common.logger import Logger
from MaKaC.common.contextManager import ContextManager

from xml.dom import minidom

from urllib import urlencode
import urllib2

from MaKaC.plugins.base import PluginsHolder
from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
from repoze.catalog.query import *


from datetime import datetime
import time
from pytz import timezone
import MaKaC.common.info as info
import Utils as u

SEA = SEATranslator("repozer")

#plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
#print "DBinit",plugin.getOptions()["DBinit"].getValue()

class RepozerSearchResult(SearchResult):
    @classmethod
    def create(cls, entryId, title, location, startDate, materials, authors, description):
        return ConferenceEntryRepozer(entryId, title, location, startDate, materials, authors, description)

class ConferenceEntryRepozer(ConferenceEntry):
    def getDescriptionText(self):        
        # this is to avoid partial HTML 
        return u.getTextFromHtml(self.getDescription())

class RepozerBaseSEA:
    _id = "repozer"

    def __init__(self, **params):
        self._userLoggedIn = params.get("userLoggedIn", False)
        self._target = params.get("target", None)
        self._page = params.get("page", 1)
        self._noQuery = False
        # this is used also as query limit. default was 25. 
        # WARNING: paging needs to be implemented
        self._pagination = 5000

        if self._userLoggedIn:
            self._sessionHash = '%s_%s' % (session.sid, session.user.getId())
        else:
            self._sessionHash = 'PUBLIC'


        self._searchCategories = False
        
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        self._DBpath = plugin.getOptions()["DBpath"].getValue()    




    def isSearchTypeOnlyPublic(self):
        #return self.getVarFromPluginStorage("type") != "private"
        return True

    
    @SEA.translate ('f',[],'p')
    def translateFieldAuthor(self, field):
        if field == "author":
            return "author:"
        else:
            return ""

    @SEA.translate ('p', 'text', 'p')
    def translatePhrase(self, phrase):
        return phrase

    @SEA.translate(['startDate', 'endDate'],'date', 'p')
    def translateDates(self, startDate, endDate):

        if startDate != '':
            startDate = time.strftime("%Y-%m-%d", time.strptime(startDate, "%d/%m/%Y"))
        if endDate != '':
            endDate = (datetime.datetime.strptime(endDate, "%d/%m/%Y") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


        if startDate != '' and endDate != '':
            return '"%s"->"%s"' % (startDate, endDate)
        elif startDate != '':
            return '"%s"->"2100"' % (startDate)
        elif endDate != '':
            return '"1950"->"%s"' % (endDate)
        else:
            return ""

    @SEA.translate ('f',[],'f')
    def translateField(self, field):
        if field == "author":
            return ""
        else:
            return field

    @SEA.translate ('startRecord',[],'jrec')
    def translateStartRecord(self, startRecord):
        return startRecord

    @SEA.translate ('numRecords',[],'rg')
    def translateNumRecords(self, numRecords):
        return numRecords

    @SEA.translate ('sortField',[],'sortField')
    def translateSortField(self, sortField):
        return sortField

    @SEA.translate ('sortOrder',[],'sortOrder')
    def translateSortOrder(self, sortOrder):
        return sortOrder

    @SEA.translate ('category', 'text', 'category')
    def translateCategory(self, phrase):
        return phrase
    
    @SEA.translate ('keywords', 'text', 'keywords')
    def translateKeywords(self, keywords):
        return keywords  
                

class RepozerSEA(RepozerBaseSEA, SearchEngineCallAPIAdapter):
    """
        Search engine adapter for Repoze.
    """
    _implementationPackage = indico.ext.search.repozer

    def __init__(self, **params):
        RepozerBaseSEA.__init__(self, **params)



    def _processElem(self, elementId):

        authors = []
        materials = []
        
        ch = conference.ConferenceHolder()
        conf = ch.getById(elementId)
        title = conf.getTitle()
        location = conf.getLocation()
        startDate = conf.getStartDate().replace(tzinfo=None)
        #materials = conf.getMaterialList()        
        
        for mat in conf.getAllMaterialList():
            url = conf.getURL() + '/material/' + mat.getId()
            materials.append((url, mat.getDescription()))    
        #print "MAT=",materials
        description = conf.getDescription()  
        for contrib in conf.getContributionList():
            if not isinstance(contrib.getCurrentStatus(),conference.ContribStatusWithdrawn):
                for auth in contrib.getAuthorList():
                    authors.append(auth)

        return RepozerSearchResult.create(elementId, title, location, startDate, materials, authors, description)



    def preProcess(self, results):
        result = []
        for res in results:
            result.append(self._processElem(res))
        return result


    def _loadBatchOfRecords(self, user, collection, number, start):

        record = start

        # by default, we should have several pages of results
        shortResult = False

        # if we're searching the private repository,
        # always request twice the number of items per page
        # (in order to account for invisible records)
        if self._userLoggedIn:
            numRequest = number * 2
        else:
            # ask always for an extra one, in order
            # to know if we reached the end
            numRequest = number+1

        results, fResults = [], []

        while (len(fResults) < number):

            Logger.get("search").debug("asking %s->%s from server (%s)" % (start, numRequest, collection))

            (r, numHits) = self.obtainRecords(startRecord=start,
                                                   numRecords=numRequest,
                                                   collections=collection,
                                                   startDate = self._filteredParams['startDate'],
                                                   endDate = self._filteredParams['endDate'],
                                                   category = self._filteredParams['category'],
                                                   keywords = self._filteredParams['keywords'],
                                                   p = self._filteredParams['p'],
                                                   f = self._filteredParams['f'],
                                                   sortField = self._filteredParams['sortField'],
                                                   sortOrder = self._filteredParams['sortOrder'])
            results.extend(r)

            # filter
            allResultsFiltered = False
            for r in results:
                if len(fResults) == number or len(fResults) == numHits:
                    break
                if r.isVisible(user):
                    fResults.append(r)
                record += 1
            else:
                allResultsFiltered = len(fResults) > 0

            if record > numHits or numHits <= number or len(results) <= number or (allResultsFiltered and len(fResults) <= number):
                shortResult = True
                break

            Logger.get("search").debug("fResults (%s)" % len(fResults))

            start += numRequest

        Logger.get("search").debug("%s %s %s" % (len(fResults), numHits, number))

        return (fResults, numHits, shortResult, record)


    def obtainRecords(self,**kwargs):
        """
            The main processing cycle. Translates the search request parameters
            from the web interface to those of the target search engine.

            @param kwargs: Input parameters

        """

        
        Logger.get('search.SEA').debug('Translating parameters...')
        #finalArgs = self.translateParameters(kwargs)
        finalArgs = kwargs

        Logger.get('search.SEA').debug('Fetching results...')
        (preResults, numPreResults) = self._fetchResultsFromServer(finalArgs )

        Logger.get('search.SEA').debug('Preprocessing results...')
        results = self.preProcess(preResults)

        Logger.get('search').debug('Done!')

        return (results, numPreResults)

    def _fetchResultsFromServer(self, parameters):

        factory = FileStorageCatalogFactory(self._DBpath,'indico_catalog')
        manager = ConnectionManager()
        catalog = factory(manager)       
        
        title = ''
        titleWilcard = ''
        startDate = None
        endDate = None
        sortField = 'startDate'
        sortReverse = True
        categories = []
        keywords = []
        tz = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        #print "PARAM=",parameters

        if parameters['p'] != '':
            title = parameters['p']
            ts = title.split(" ")
            titleWilcard = "*"+"* *".join(ts)+"*"
            #print titleWilcard
        if parameters['startDate'] != '':
            sdd,sdm,sdy = parameters['startDate'].split('/')
            startDate = timezone(tz).localize(datetime( int(sdy), int(sdm), int(sdd), 0, 0 ))  
        if parameters['endDate'] != '':
            sdd,sdm,sdy = parameters['endDate'].split('/')
            endDate = timezone(tz).localize(datetime( int(sdy), int(sdm), int(sdd), 0, 0 ))     
        if parameters['sortOrder'] == 'a':
            sortReverse = False
        if parameters['sortField'] != '':
            sortField = parameters['sortField']
        if parameters['keywords'] != '':
            keywords = parameters['keywords'].split(',')     

        
        # Ictp specific: just replace with your custom dictionary or
        # with: categories = parameters['category'].split(',')      
        if parameters['category'] != '':
            dict_cat = {'Activities in Trieste':'ICTP activities in Trieste',
                'Activities outside Trieste':'ICTP activities outside Trieste',
                'Seminars':'Hosted activities',
                'Hosted activities':'Hosted activities'}
            for cat in parameters['category'].split(','):
                categories.append(dict_cat[cat])
            
            
        ##### EXECUTE QUERY #####
        
        if parameters['f'] == '':
            query = Eq('title', titleWilcard)
        elif parameters['f'] == 'title_description': 
            query = Eq('description', titleWilcard) | Eq('title', titleWilcard)
        elif parameters['f'] == 'roles':
            query = Contains('rolesVals', title)                
        if (categories != []):
            query = query & Any('category', categories)        
        if (keywords != []):
            query = query & Any('keywords', keywords)
                            
        query = query & InRange('startDate',startDate, endDate)    
        numdocs, results = catalog.query(query, sort_index=sortField, reverse=sortReverse, limit=self._pagination)

        # Ictp specific: have to replace 9999 with 'a' 
        res = []
        for r in results:
            if str(r).startswith('9999'): res.append(str(r).replace('9999','a'))
            else: res.append(str(r))                
        
        factory.db.close()
        
        return (res, numdocs)


    def _getResults(self, collection, number):

        params = copy.copy(self._filteredParams)
        params['collections'] = collection
        params['target'] = self._target.getId()

        queryHash = self._getQueryHash(params)

        Logger.get('search').debug('Hashing %s to %s' % (params, queryHash))

        # ATTENTION: _getStartingRecord will set self._page to 1,
        # if there's a cache miss
        start, cachedObj = self._getStartingRecord(queryHash, self._page)

        # get the access wrapper, so we can check user access privileges
        user = ContextManager.get("currentRH", None).getAW()

        results, numHits, shortResult, record = self._loadBatchOfRecords(user, collection, number, start)

        self._cacheNextStartingRecord(queryHash, self._page, record, cachedObj)

        return (numHits, shortResult, record, results)

    def process(self, filteredParams):

        self._filteredParams = filteredParams
        phrase = self._filteredParams.get('p', '')
        if phrase.strip() == '':
            self._noQuery = True

        params = copy.copy(self._filteredParams)
        
        # right now, I want to search ONLY in Events, so I force it
        params['collections'] = 'Events'

        nEvtRec, nContRec = 0, 0
        numEvtHits, numContHits = 0, 0
        eventResults, contribResults = [], []
        
        if not self._noQuery:
            if params.get('collections',"") != 'Contributions':
                numEvtHits, evtShortResult, nEvtRec, eventResults = self._getResults('Events', self._pagination)
                params['evtShortResult'] = evtShortResult

            if params.get('collections',"") != 'Events':
                numContHits, contShortResult, nContRec, contribResults = self._getResults('Contributions', self._pagination)
                params['contShortResult'] = contShortResult

        params['p'] = cgi.escape(phrase, quote=True)
        params['f'] = cgi.escape(filteredParams.get('f', ''), quote=True)

        params['eventResults'] = eventResults
        params['contribResults'] = contribResults
        

        params['nEventResult'] = nEvtRec
        params['nContribResult'] = nContRec

        params['numHits'] = numEvtHits + numContHits
        params['page'] = self._page

        params['targetObj'] = self._target

        params['searchingPublicWarning'] = self.isSearchTypeOnlyPublic() and not self._userLoggedIn
        params['accessWrapper'] = ContextManager().get("currentRH", None).getAW()

        return params
