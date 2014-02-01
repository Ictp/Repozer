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

from MaKaC.conference import CategoryManager, ConferenceHolder
from MaKaC.plugins.base import PluginsHolder
from indico.ext.search.repozer import Utils as ut
from indico.ext.search.repozer.options import typesToIndicize
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *
import transaction
# This is for using with external DB
#from repoze.catalog.catalog import FileStorageCatalogFactory
#from repoze.catalog.catalog import ConnectionManager
#from persistent import Persistent
#from BTrees.OOBTree import OOBTree


db.DBMgr.getInstance().startRequest()

# This is for using with external DB
#plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
#DBpath = plugin.getOptions()["DBpath"].getValue() 
#factory = FileStorageCatalogFactory(DBpath, 'repoze_catalog')

rc = RepozeCatalog()


def buildCatalog():
    # Force indexes creation
    rc.init_catalog()
    #manager = ConnectionManager()
    #catalog = factory(manager)
    cm = CategoryManager()
    totnum = len(cm.getList())
    curnum = 0
    curper = 0
        
    for cat in cm.getList():
        for conf in cat.getConferenceList():
            # Check if conference REALLY exist:
            ch = ConferenceHolder()
            c = None
            try:
                c = ch.getById(conf.id)
            except:
                print "Conference ",conf.id," not indexed"
                pass
            if (c != None):                
                c._catName = [str(cat.name)]                
                rc.index(c)                
        
        transaction.commit()

        curnum += 1
        per = int(float(curnum)/float(totnum)*100)
        if per != curper:
            curper = per
            print "%s%%" % per
            
    #rc.closeConnection()
    # Pack it when finished
    print "Packing...."
    #rc.factory.db.pack()
    db.DBMgr.getInstance().pack()
    #rc.closeConnection()
    
    print "Done."
    
    db.DBMgr.getInstance().endRequest()


if __name__ == '__main__':     
    buildCatalog()
    # QUERY TEST
    #query = Eq('title', 'Ictp') & Any('collection', ['Conference'])
    #numdocs, results = rc.catalog.query(query)
    #rc.closeConnection()
    #print "QUERY RES=",numdocs,results
    
