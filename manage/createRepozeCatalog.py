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
from repoze.catalog.document import DocumentMap
 
import transaction
from persistent import Persistent
from BTrees.OOBTree import OOBTree

from MaKaC.plugins.base import PluginsHolder
from indico.ext.search.repozer import Utils as ut


from MaKaC.webinterface import urlHandlers

from indico.ext.search.repozer.options import typesToIndicize
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *



db.DBMgr.getInstance().startRequest()
#plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
#DBpath = plugin.getOptions()["DBpath"].getValue() 

initialized = False
#factory = FileStorageCatalogFactory(DBpath, 'indico_catalog')

rc = RepozeCatalog()
                                    
def initialize_catalog():
    '''
    Create a repoze.catalog instance and specify
    indices of intereset
    '''
    global initialized
    global factory
    
    if not initialized:
        # create a catalog
        #manager = ConnectionManager()
        #catalog = factory(manager)
        
        rc.catalog.document_map = DocumentMap()
                
        # set up indexes
        rc.catalog['title'] = CatalogTextIndex('_get_title')
        rc.catalog['titleSorter'] = CatalogFieldIndex('_get_sorter')
        rc.catalog['collection'] = CatalogKeywordIndex('_get_collection')
        # Descriptions are converted to TEXT for indexing
        rc.catalog['description'] = CatalogTextIndex('_get_description')
        rc.catalog['startDate'] = CatalogFieldIndex('_get_startDate')
        rc.catalog['endDate'] = CatalogFieldIndex('_get_endDate')
        rc.catalog['keywords'] = CatalogKeywordIndex('_get_keywordsList')
        rc.catalog['category'] = CatalogKeywordIndex('_catName')
        # I define as Text because I would permit searched for part of names
        rc.catalog['rolesVals'] = CatalogTextIndex('_get_roles')
        rc.catalog['person'] = CatalogTextIndex('_get_person')
        
        # commit the indexes
        rc.manager.commit()
        #manager.close()
        initialized = True





def buildCatalog():
    initialize_catalog()
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
#                 if 'Conference' in typesToIndicize:
#                     RepozeCatalog().indicizeConference(c, catalog)
# 
#                 if 'Contribution' in typesToIndicize:
#                     for talk in conf.getContributionList():
#                         talk._catName = [str(cat.name)]                  
#                         RepozeCatalog().indicizeContribution(talk, catalog)
#                 
#                 #if 'Material' in typesToIndicize and conf.getId() not in ['a1311','a13181','a12225','a1317','a12224']:
#                 #if conf.getId() == 'a12163':
#                 if 'Material' in typesToIndicize:
#                     for mat in conf.getAllMaterialList():
#                         #murl = conf.getURL() + '/material/' + mat.getId()
#                         mat._catName = c._catName
#                         mat._roles = []
# 
#                         for res in mat.getResourceList():
#                             ftype = res.getFileType()
#                             fname = res.getFileName()
#                             fpath = res.getFilePath()
#                             #furl = urlHandlers.UHFileAccess.getURL(res)
#                             content = ''
#                             if ftype == 'PDF':                            
#                                 try:
#                                     pdf = pyPdf.PdfFileReader(open(fpath, "rb"))
#                                     for page in pdf.pages:
#                                         content += ' '+page.extractText()
#                                     
#                                 except:
#                                     # something has gone wrong
#                                     pass
#                                 mat._content = content
#                                 RepozeCatalog().indicizeMaterial(mat, catalog)
                            
                    #for mat in conf.getAllMaterialDict():
                        #print "MAT=",conf.getAllMaterialDict()["material"]
                        #print "MAT class=",mat,"---->MATERIAL=",vars(mat)
                        #url = conf.getURL() + '/material/' + mat.getId()
                        #materials.append((url, mat.getDescription())) 
                
        
        transaction.commit()

        curnum += 1
        per = int(float(curnum)/float(totnum)*100)
        if per != curper:
            curper = per
            print "%s%%" % per
            
    #rc.closeConnection()
    # Pack it when finished
    print "Packing...."
    rc.factory.db.pack()
    rc.closeConnection()
    print "Done."
    
    db.DBMgr.getInstance().endRequest()


if __name__ == '__main__':     
    buildCatalog()
    # QUERY TEST
    #query = Eq('description', 'Mathematics') & Eq('collection', ['Material'])
    #query = Eq('title', 'Ictp') & Any('collection', ['Conference'])
    #numdocs, results = rc.catalog.query(query)
    #rc.closeConnection()
    #print "QUERY RES=",numdocs,results
    
