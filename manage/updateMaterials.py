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


""" 
Use this script for Material index updates. This is needed because there is no IMaterial event hook yet.
Change the updateHours parameter to change the check time. Default is 24 Hours
We suggest to use this in cronjob.
Eg:  0 2 * * * /usr/bin/python /opt/indico/src/indico/ext/search/repozer/manage/updateMaterials.py 
"""

updateHours = 24

db.DBMgr.getInstance().startRequest()
rc = RepozeCatalog()

def updateCatalog():    
    localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
    cDate = timezone(localTimezone).localize(datetime.datetime.now() - timedelta(hours=updateHours))
    # Search for recently modified Conferences. This is very time consuming....
    results = []
    for conf in ConferenceHolder().getValuesToList():
        if conf.getModificationDate() >= cDate:
            results.append(conf)
            rc.reindex(conf, True) 
    
    if results:
        print "Updated", len(results), "Conference(s)."
            
    transaction.commit()                       
    # Pack it when finished
    #print "Packing...."
    #db.DBMgr.getInstance().pack()
    print "Done."

if __name__ == '__main__':  
    updateCatalog()
    db.DBMgr.getInstance().endRequest()
    
