# -*- coding: utf-8 -*-
##
## $id$
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

# stdlib imports
import zope.interface
import os

# legacy imports
from MaKaC.plugins.base import Observable

# indico imports
from indico.core.extpoint import Component
from indico.core.extpoint.events import IObjectLifeCycleListener, IMetadataChangeListener
from indico.core.extpoint.plugins import IPluginImplementationContributor
from indico.ext.search.repozer.implementation import RepozerSEA
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
import indico.ext.search.repozer
from MaKaC.plugins.base import PluginsHolder
from indico.web.handlers import RHHtdocs
import inspect
from repozeIndexer import RepozeCatalog
from indico.ext.search.register import SearchRegister
from zope.interface import implements

import MaKaC.services.implementation.conference as conference

from indico.ext.search.repozer.options import typesToIndex
import hashlib, pickle



def toIndex(obj):
    plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
    liveUpdate = plugin.getOptions()["liveUpdate"].getValue()
    return liveUpdate and type(obj).__name__ in typesToIndex and not(obj.hasAnyProtection())



# This is just until ROLES will be integrated in Indico with hook on event listener
defclasses = []
for name, obj in inspect.getmembers(conference, inspect.isclass):
    defclasses.append(name)
if 'ConferenceRolesModification' in defclasses:
    class ConferenceRolesModificationRepozer(conference.ConferenceRolesModification):
        """
        Conference roles modification
        """
        
        def _handleSet(self):
            if toIndex(obj):
                conference.ConferenceRolesModification._handleSet(self)
                rc = RepozeCatalog()
                rc.reindex(self._target)
                rc.closeConnection()
        self._target.setRoles(self._value)
    conference.methodMap["main.changeRoles"] = ConferenceRolesModificationRepozer



# This should be removed...
# Class override from /MaKaC/services/implementation/conference.py
class ConferenceKeywordsModificationRepozer( conference.ConferenceKeywordsModification ):
    """
    Conference keywords modification
    """
    

        
    def _handleSet(self):
        if toIndex(obj):
            conference.ConferenceKeywordsModification._handleSet(self)
            rc = RepozeCatalog()
            rc.reindex(self._target)
            rc.closeConnection()        
        self._target.setKeywords(self._value)    
conference.methodMap["main.changeKeywords"] = ConferenceKeywordsModificationRepozer        




class ObjectChangeListener(Component):
    """
    This component listens for events and directs them to the MPT.
    Implements ``IObjectLifeCycleListener``,``IMetadataChangeListener``
    """

    implements(IMetadataChangeListener, IObjectLifeCycleListener)

#     def getHash(self, obj):
#         arr = [str(getattr(obj, x)).decode('utf8','ignore') for x in vars(obj).keys() if x != '_modificationDS']
#         return ''.join(arr)
        


    def created(self, obj, owner):
        if toIndex(obj):
            rc = RepozeCatalog()
            #obj.md5 = self.getHash(obj)
            rc.index(obj)
            rc.closeConnection()

    def moved(self, obj, fromOwner, toOwner):
        if toIndex(obj):
            rc = RepozeCatalog()
            rc.reindex(obj)
            rc.closeConnection()

    def deleted(self, obj, oldOwner):
        if toIndex(obj):
            rc = RepozeCatalog()
            rc.unindex(obj)
            rc.closeConnection()        
            
    def eventTitleChanged(self, obj, oldTitle, newTitle):
        if toIndex(obj):
            rc = RepozeCatalog()
            rc.reindex(obj)
            rc.closeConnection()
            
    def infoChanged(self, obj):
        if toIndex(obj):
            #print "...indexing..."
            rc = RepozeCatalog()
            # I dont want to reindex Material, it takes soo long
            rc.reindex(obj,False)
            rc.closeConnection()
                            
    def eventDatesChanged(cls, obj, oldStartDate, oldEndDate, newStartDate, newEndDate):
        if toIndex(obj):
            rc = RepozeCatalog()
            rc.reindex(obj)
            rc.closeConnection()                          

class PluginImplementationContributor(Component, Observable):
    """
    Adds interface extension to plugins's implementation.
    """

    zope.interface.implements(IPluginImplementationContributor)
        
    def getPluginImplementation(self, obj):
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        #liveUpdate = plugin.getOptions()["liveUpdate"].getValue()
        #typeSearch = plugin.getOptions()["type"].getValue()
        return ("repozer", RepozerSEA)


class RHSearchHtdocsRepozer(RHHtdocs):

    _local_path = os.path.join(os.path.dirname(indico.ext.search.repozer.__file__), "htdocs")
    _min_dir = 'repozer'
