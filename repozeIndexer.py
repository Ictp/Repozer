# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.

from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
from MaKaC.plugins.base import PluginsHolder
import transaction

from Utils import getRolesValues
from lxml import html

typesToIndicize = ['Conference']

class RepozeCatalog():

    def __init__(self):
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        DBpath = plugin.getOptions()["DBpath"].getValue()
        self.factory = FileStorageCatalogFactory(DBpath,'indico_catalog')
        self.manager = ConnectionManager()
        self.catalog = self.factory(self.manager)
    
    def toIndicize(obj):
        return type(obj).__name__ in typesToIndicize
    
    def fixIndexes(self, c):
        c._intId = int(str(c.getId()).replace('a',''))
        c._listKeywords = c._keywords.split('\n')
        c._rolesVals = getRolesValues(c)
        c._titleSorter = str(c.title).lower().replace(" ", "")
        try:
            s = html.fromstring(c.getDescription()).text_content()
            s = s.encode('ascii','ignore')
        except:
            s = c.getDescription()
        c._descriptionText = s
                
    def index(self, c):
        if self.toIndicize(c):
            self.fixIndexes(c)
            #c._catName = categoria di appartenenza
            print "*****Indexing:",type(c).__name__
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
