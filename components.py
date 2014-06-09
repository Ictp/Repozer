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

import hashlib, pickle



def toIndex(obj):
    plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
    if type(obj).__name__ == 'Conference':
        return plugin.getOptions()["indexConference"].getValue()
    if type(obj).__name__ == 'Contribution':
        return plugin.getOptions()["indexContribution"].getValue()
    if type(obj).__name__ == 'LocalFile':
        return plugin.getOptions()["indexMaterial"].getValue()
    return False


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
            conference.ConferenceRolesModification._handleSet(self)
            if toIndex(self._target):                
                rc = RepozeCatalog()
                rc.unindexObject(self._target)
                rc.indexObject(self._target)
                rc.closeConnection()
    conference.methodMap["main.changeRoles"] = ConferenceRolesModificationRepozer



# This should be removed...
# Class override from /MaKaC/services/implementation/conference.py
class ConferenceKeywordsModificationRepozer( conference.ConferenceKeywordsModification ):
    """
    Conference keywords modification
    """
        
    def _handleSet(self):
        conference.ConferenceKeywordsModification._handleSet(self)
        if toIndex(self._target):            
            rc = RepozeCatalog()
            rc.unindexObject(self._target)
            rc.indexObject(self._target)            
            rc.closeConnection()        
conference.methodMap["main.changeKeywords"] = ConferenceKeywordsModificationRepozer        




class ObjectChangeListener(Component):
    """
    This component listens for events and directs them to the MPT.
    Implements ``IObjectLifeCycleListener``,``IMetadataChangeListener``
    """

    implements(IMetadataChangeListener, IObjectLifeCycleListener)

    def deleted(self, obj, oldOwner):
        print "___DELETED CALL OBJ=",obj, oldOwner
        if toIndex(obj):
            rc = RepozeCatalog()
            # Use recursion
            rc.unindexObject(obj, True)
            oldOwner._notify('deleted', obj)
            rc.closeConnection() 
                   
                        
    def infoChanged(self, obj):
        print "___INFO CHANGED", obj
        if toIndex(obj):
            rc = RepozeCatalog()
            rc.unindexObject(obj)
            rc.indexObject(obj)
            rc.closeConnection()
            

    def created(self, obj, owner):
        pass
    def moved(self, obj, fromOwner, toOwner):
        pass
    def eventTitleChanged(self, obj, oldTitle, newTitle):
        pass                            
    def eventDatesChanged(cls, obj, oldStartDate, oldEndDate, newStartDate, newEndDate):
        pass


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
