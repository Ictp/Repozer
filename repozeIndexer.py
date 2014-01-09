# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.

from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
from MaKaC.plugins.base import PluginsHolder
from MaKaC.conference import ConferenceHolder
import transaction
import Utils as u

class RepozeCatalog():

    def __init__(self):
        pass
    
    def fixIndexes(self, c):
        c._intId = int(str(c.getId()).replace('a','9999'))
        c._listKeywords = c._keywords.split('\n')
        c._rolesVals = u.getRolesValues(c)
        c._titleSorter = str(c.title).lower().replace(" ", "")
        c._descriptionText = u.getTextFromHtml(c.getDescription())
                
    def index(self, c):
        self.openConnection()
        self.fixIndexes(c)
        #c._catName = categoria di appartenenza
        self.catalog.index_doc(c._intId, c)
        self.closeConnection(c)

    def unindex(self, c):   
        self.openConnection()     
        intId = int(str(c.getId()).replace('a','9999'))
        self.catalog.unindex_doc(intId)
        self.closeConnection(c)
        
    def reindex(self, c):
        self.openConnection()     
        # Check if conference still exist
        ch = ConferenceHolder()        
        cc = None
        try: cc = ch.getById(c.id)
        except: pass            
        if cc:
            self.fixIndexes(c)
            self.catalog.reindex_doc(c._intId, c)        
        self.closeConnection(c)        
        
    def closeConnection(self, c):
        transaction.commit()              
        self.factory.db.close()
        self.manager.commit()        
        self.manager.close() 

    def openConnection(self):
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        DBpath = plugin.getOptions()["DBpath"].getValue()
        self.factory = FileStorageCatalogFactory(DBpath,'indico_catalog')
        self.manager = ConnectionManager()
        self.catalog = self.factory(self.manager)
