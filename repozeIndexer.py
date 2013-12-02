# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.

# OP ADDED: INDEX NEW CONFERENCE
from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
import transaction
#from repoze.catalog.query import *
from MaKaC.plugins.base import PluginsHolder

from Utils import getRolesValues
import html2text

plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
DBpath = plugin.getOptions()["DBpath"].getValue()
indicize = True

class RepozeCatalog():

    def __init__(self):
        if indicize:
            self.factory = FileStorageCatalogFactory(DBpath,'indico_catalog')
            self.manager = ConnectionManager()
            self.catalog = self.factory(self.manager)
    
    def fixIndexes(self, c):
        c._intId = int(c.getId().replace('a',''))
        c._listKeywords = c._keywords.split('\n')
        c._rolesVals = getRolesValues(c)
        c._titleSorter = str(c.title).lower().replace(" ", "")
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        try:
            s = h.handle(c.getDescription().decode('utf8','ignore'))
            s = s.encode('ascii','ignore')
        except:
            s = c.getDescription()
        c._descriptionText = s
                
    def index(self, c):
        if indicize:
            self.fixIndexes(c)
            #c._catName = categoria di appartenenza
            self.catalog.index_doc(c._intId, c)
            self.closeConnection()

    def unindex(self, c):
        if indicize:
            intId = int(c.getId().replace('a',''))
            self.catalog.unindex_doc(intId)
            self.closeConnection()
        
    def reindex(self, c):
        if indicize:
            self.fixIndexes(c)
            self.catalog.reindex_doc(c._intId, c)        
            self.closeConnection()        
        
    def closeConnection(self):
        if indicize:
            transaction.commit()              

        self.factory.db.close()
        self.manager.commit()        
        self.manager.close() 