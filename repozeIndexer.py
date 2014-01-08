# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.

from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
from MaKaC.plugins.base import PluginsHolder
import transaction
import Utils as u

typesToIndicize = ['Conference']

class RepozeCatalog():

    def __init__(self):
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        DBpath = plugin.getOptions()["DBpath"].getValue()
        self.factory = FileStorageCatalogFactory(DBpath,'indico_catalog')
        self.manager = ConnectionManager()
        self.catalog = self.factory(self.manager)
    
    def toIndicize(self,obj):
        return type(obj).__name__ in typesToIndicize
    
    def fixIndexes(self, c):
        c._intId = int(str(c.getId()).replace('a',''))
        c._listKeywords = c._keywords.split('\n')
        c._rolesVals = u.getRolesValues(c)
        c._titleSorter = str(c.title).lower().replace(" ", "")
        c._descriptionText = u.getTextFromHTML(c.getDescription())
                
    def index(self, c):
        if self.toIndicize(c):
            self.fixIndexes(c)
            #c._catName = categoria di appartenenza
            self.catalog.index_doc(c._intId, c)
        self.closeConnection(c)

    def unindex(self, c):
        if self.toIndicize(c):
            intId = int(c.getId().replace('a',''))
            self.catalog.unindex_doc(intId)
        self.closeConnection(c)
        
    def reindex(self, c):
        if self.toIndicize(c):
            self.fixIndexes(c)
            self.catalog.reindex_doc(c._intId, c)        
        self.closeConnection(c)        
        
    def closeConnection(self, c):
        if self.toIndicize(c):
            transaction.commit()              
        self.factory.db.close()
        self.manager.commit()        
        self.manager.close() 
