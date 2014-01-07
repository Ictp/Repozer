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

try:
    from indico.core import db
except:
    from MaKaC.common import db

from MaKaC.conference import CategoryManager, ConferenceHolder

from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
 
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
 
import transaction
from persistent import Persistent
from BTrees.OOBTree import OOBTree


from MaKaC.plugins.base import PluginsHolder
from indico.ext.search.repozer.Utils import getRolesValues

#import indico.ext.search.repozer.html2text as html2text
from lxml import html

db.DBMgr.getInstance().startRequest()
plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
DBpath = plugin.getOptions()["DBpath"].getValue() 

_initialized = False
factory = None

def initialize_catalog():
    '''
    Create a repoze.catalog instance and specify
    indices of intereset
 
    NB: Use of global variable
    '''
    global _initialized
    global factory
    factory = FileStorageCatalogFactory(DBpath, 'indico_catalog')
    if not _initialized:
        # create a catalog
        manager = ConnectionManager()
        catalog = factory(manager)
        
        # set up indexes
        #### CHANGE HERE TO ADD OR REMOVE INDEXES!!!
        catalog['title'] = CatalogTextIndex('title')
        catalog['titleSorter'] = CatalogFieldIndex('_titleSorter')
        # Descriptions is converted to TEXT for indexing
        catalog['description'] = CatalogTextIndex('_descriptionText')
        catalog['startDate'] = CatalogFieldIndex('startDate')
        catalog['endDate'] = CatalogFieldIndex('endDate')
        catalog['keywords'] = CatalogKeywordIndex('_listKeywords')
        catalog['category'] = CatalogKeywordIndex('_catName')
        # I define rolesVals as Text because I would permit searched for part of names
        catalog['rolesVals'] = CatalogTextIndex('_rolesVals')

        # commit the indexes
        manager.commit()
        manager.close()
        _initialized = True



def buildCatalog(DBpath):

    initialize_catalog()
    manager = ConnectionManager()
    catalog = factory(manager)
    
    # START EXISTING CONTENT INDEXING
    ch = CategoryManager()
    totnum = len(ch.getList())
    curnum = 0
    curper = 0
    for cat in ch.getList():
        for conf in cat.getConferenceList():
            # Check if conference REALLY exist:
            ch = ConferenceHolder()
            #fetch the conference which type is to be updated
            c = None
            try:
                c = ch.getById(conf.id)
            except:
                print "Conference ",conf.id," not indexed"
                pass
            if (c != None):
                # Ictp conferences Id starts with an 'a' char: need to be removed
                intId = int(str(conf.getId()).replace('a','9999'))
                conf._catName = [str(cat.name)]            
                if len(conf._keywords)>0: 
                    conf._listKeywords = conf._keywords.split('\n')
                #conf._catId = cat.id            
                conf._rolesVals = getRolesValues(conf) 
                conf._titleSorter = str(conf.title).lower().replace(" ", "") 
            
                s = ''
                if conf.getDescription(): 
                    try:
                        s = html.fromstring(conf.getDescription().decode('utf8','ignore')).text_content()
                        s = s.encode('ascii','ignore')
                    except: 
                        s = conf.getDescription()
                conf._descriptionText = s
                catalog.index_doc(intId, conf)
        transaction.commit()
        curnum += 1
        per = int(float(curnum)/float(totnum)*100)
        if per != curper:
            curper = per
            print "%s%%" % per
            
    # Pack it when finished
    print "Packing...."
    factory.db.pack()
    factory.db.close()
    
    manager.commit()
    manager.close()
    print "Done."
    
    db.DBMgr.getInstance().endRequest()


if __name__ == '__main__':
     
    buildCatalog(DBpath)  
