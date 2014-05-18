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

try: from indico.core import db
except: from MaKaC.common import db

from MaKaC.conference import ConferenceHolder

from indico.ext.search.repozer import Utils as ut
import MaKaC.common.info as info
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *
import transaction
from datetime import datetime, timedelta
from pytz import timezone, utc
from MaKaC.conference import CustomRoom
import json



db.DBMgr.getInstance().startRequest()
rc = RepozeCatalog()

localTimezone = 'Europe/Rome'
from pytz import timezone

def updateCatalog():    
    # Search for recently modified Conferences. This is very time consuming....
    results = []
    i=0
    for conf in ConferenceHolder().getValuesToList():
        i+=1
        confId = conf.getId()


        
        if 1:
            keyw = conf.getKeywords().split("\n")
            for keyword in keyw:
                if not(keyword in results) and not(keyword.startswith('smr')) and not(keyword.startswith('expparts')) and not(keyword.startswith('siscode')) and keyword != '':
                    results.append(keyword)
            
    print results 
        
        
        #print "confId=",confId
        # select Conference in AGENDA:
        #if confId == 'a13297':
        #    print "cat=",conf._get_categoryList   
        
        #if '2l133' in conf._get_categoryList:        
        #    print "cat=",conf._get_categoryList
        
        #cc.execute("set character set utf8")
        #cc.execute("select * from AGENDA where id='%s'" % confId)
        #confAgenda = cc.fetchone()
        #while confAgenda != None:
        #if confAgenda != None:
            #confAgenda = cc.fetchone()
        #    print confAgenda
        #    confAgenda = cc.fetchone()

    #cc.execute("set character set utf8")
    #cc.execute("select * from AGENDA where fid in ('%s') and id>='' order by id"%strlistcat)
    #s = cc.fetchone()    
    #while s!=None:
    #    s = cs.fetchone() # next
    
                    
    #transaction.commit()                       
    # Pack it when finished
    #print "Packing...."
    #db.DBMgr.getInstance().pack()
    print "Done."

if __name__ == '__main__':  
    updateCatalog()
    db.DBMgr.getInstance().endRequest()
    
