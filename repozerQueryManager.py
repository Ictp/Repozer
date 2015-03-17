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

from MaKaC.conference import ConferenceHolder
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from indico.ext.search.repozer.options import confCatalog, contribCatalog, matCatalog

from datetime import datetime
import time
from pytz import timezone
import MaKaC.common.info as info

from repoze.catalog.query import *


class RepozerQueryManager():    
    
    def __init__(self, params):
        self.query = None
        self.params = params
        


    def getQuery(self):        
        if not self.params:
            return        
        self.checkParams()                                 
        return self.query


    def setQuery(self, query):
        self.query = query
        

    def addQuery(self, elem):
        if not self.query:
            self.query = elem
        else:
            self.query = self.query & elem
        return
                
        
    def getResults(self, query=None):
        res = []
        params = self.params

        if params.get('id',None):
            event = ch.getById(params['id'])
            res.append(event)
            return 1, res
        
        if not query:
            query = self.getQuery() 
        
        if not query:
            return 0, []
        
        collections = params.get('collections', 'Conference')
        rc = RepozeCatalog()
        if collections == 'Material':
            rc = RepozeCatalog(matCatalog)
        if collections == 'Contribution':
            rc = RepozeCatalog(contribCatalog)
                    
        catalog = rc.catalog    
        ch = ConferenceHolder()                
        desc = params.get('desc',False)  
        sort_field = params.get('sort_field','startDate')  
        
        numdocs, results = catalog.query(query, sort_index=sort_field, reverse=desc, limit=params.get('limit',5000))                    
        results = [catalog.document_map.address_for_docid(result) for result in results]
        
        if params.get('onlyFids', False):
            return numdocs, results
        else:
            for obj in results:
                try:
                    confId = str(obj).split("|")[0]
                    event = ch.getById(confId)
                    res.append(event)
                except:
                    pass        
                                                    
        return numdocs, res
        
            
    def checkParams(self):        
        params = self.params         

        if params.has_key('text'):
            text = params.get('text', None)
            
            # Ictp: custom case
            if text.lower().startswith('smr'):
                self.setQuery( Any('keywords', text.strip()) )
                return
                       
            # WHERE: specify where to search       
            where = params.get('where', 'title_description')
            if where == 'title_description':
                self.addQuery( Eq('title', text.decode('utf8')) | Eq('description', text.decode('utf8')) )

            if where == 'title':
                self.addQuery( Eq('title', text.decode('utf8')) )
                
            if where == 'roles':
                val = unicode(text, "UTF-8").encode('ascii', 'xmlcharrefreplace')
                self.addQuery( Contains('rolesVals', val) )
                
            if where == 'persons':
                self.addQuery( Contains('persons', text.decode('utf8')) )

            if where == 'all':
                val = unicode(text, "UTF-8").encode('ascii', 'xmlcharrefreplace')
                textDecoded = text.decode('utf8')
                self.addQuery( Eq('description', textDecoded) | Eq('title', textDecoded) | Contains('persons', text) | Contains('rolesVals', val) )
                

        # START_DATE, END_DATE, STARTED
        startDate_ts = None
        endDate_ts = None
        datesAvailable = False
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        
        if params.has_key('start_date'):
            sdate = params['start_date'].split('/')
            if 1:
            #try:
                startDate_ts = timezone(localTimezone).localize(datetime(int(sdate[0]), int(sdate[1]), int(sdate[2]), 0, 0))
                datesAvailable = True
            #except:
            #    self.setQuery(None)
            #    return
         
        if params.has_key('end_date'):
            edate = params['end_date'].split('/')
            try:
                endDate_ts = timezone(localTimezone).localize(datetime(int(edate[0]), int(edate[1]), int(edate[2]), 23, 59))
                datesAvailable = True
            except:
                self.setQuery(None)
                return                
            
        if params.has_key('started'):
            ssdate = params['started'].split('/')
            try:
                started_ts = timezone(localTimezone).localize(datetime(int(ssdate[0]), int(ssdate[1]), int(ssdate[2]), 0, 0))
                self.addQuery( Ge('startDate',started_ts) )
            except:
                self.setQuery(None)
                return
                
        elif params.has_key('today'):
            if params['today'] == '':
                td = time.strftime("%Y/%m/%d").split('/')
            else:                
                td = params['today'].split('/')
            try:
                today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 23, 59))
                end_today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 00, 00))
            except:
                self.setQuery(None)
                return               
            self.addQuery( Le('startDate',today_ts) & Ge('endDate',end_today_ts) )
            
        elif params.has_key('todaybeyond'):
            if params['todaybeyond'] == '':
                td = time.strftime("%Y/%m/%d").split('/')
            else:                
                td = params['todaybeyond'].split('/')
            try:
                today_ts = timezone(localTimezone).localize(datetime(int(td[0]), int(td[1]), int(td[2]), 23, 59))
            except:
                self.setQuery(None)
                return                                    
            self.addQuery( Le('startDate',today_ts) & Ge('endDate',today_ts) | Ge('startDate',today_ts) )                    
                
        elif datesAvailable:
                self.addQuery( Not(Lt('endDate',startDate_ts) | Gt('startDate',endDate_ts)) | (InRange('startDate',startDate_ts, endDate_ts)) )    
                
        if params.has_key('keywords'):
            k = params['keywords']
            if k.find(',') > -1:
                kw = k.split(',')
            else:
                kw = [k]     
            self.addQuery( Any('keywords', kw) )
        
        if params.has_key('keywordsAnd'):
            kw = params['keywordsAnd'].split(',')
            self.addQuery( All('keywords', kw) )
        
        if params.has_key('category'):
            kw = params['category']
            self.addQuery( Any('category', kw) )
        
        # ICTP SPECIFIC
        if params.has_key('valid_deadline'):
            today = datetime.now()
            self.addQuery( Gt('deadlineDate', today) & NotEq('deadlineDate', datetime.strptime('01/01/1970', '%d/%m/%Y')) )

        # ICTP SPECIFIC: do not add Conference with keyword = NOSCIAL 
        if params.get('collections', 'Conference') == 'Conference':                         
            self.addQuery( Not(Any('keywords', 'NOSCICAL')) )  

        return        
                
                


        
            