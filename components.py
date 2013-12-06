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
from indico.core.extpoint.plugins import IPluginImplementationContributor
from indico.ext.search.repozer.implementation import RepozerSEA
import indico.ext.search.repozer
from MaKaC.plugins.base import PluginsHolder
from indico.web.handlers import RHHtdocs

import inspect

# PATCH FOR INDEXING
from repozeIndexer import RepozeCatalog
def reindex(conf):
    rc = RepozeCatalog()
    rc.reindex(conf)


# Class override from /MaKaC/services/implementation/conference.py
import MaKaC.services.implementation.conference as conference

class ConferenceTitleModificationRepozer( conference.ConferenceTitleModification ):
    """
    Conference title modification
    """
    def _handleSet(self):
        conference.ConferenceTitleModification._handleSet(self)
        reindex(self._target)

class ConferenceDescriptionModificationRepozer( conference.ConferenceDescriptionModification ):
    """
    Conference description modification
    """
    def _handleSet(self):
        conference.ConferenceDescriptionModification._handleSet(self)
        reindex(self._target)


class ConferenceKeywordsModificationRepozer( conference.ConferenceKeywordsModification ):
    """
    Conference keywords modification
    """
    def _handleSet(self):
        conference.ConferenceKeywordsModification._handleSet(self)
        reindex(self._target)


class ConferenceStartEndDateTimeModificationRepozer( conference.ConferenceStartEndDateTimeModification ):
    """
    Conference start date/time modification
    """
    def _getAnswer(self):
        conference.ConferenceStartEndDateTimeModification._getAnswer(self)
        reindex(self._target)



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
            reindex(self._target)

    conference.methodMap["main.changeRoles"] = ConferenceRolesModificationRepozer



conference.methodMap["main.changeTitle"] = ConferenceTitleModificationRepozer
conference.methodMap["main.changeDescription"] = ConferenceDescriptionModificationRepozer
conference.methodMap["main.changeKeywords"] = ConferenceKeywordsModificationRepozer
conference.methodMap["main.changeDates"] = ConferenceStartEndDateTimeModificationRepozer

    





class PluginImplementationContributor(Component, Observable):
    """
    Adds interface extension to plugins's implementation.
    """

    zope.interface.implements(IPluginImplementationContributor)
        
    def getPluginImplementation(self, obj):
        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        #typeSearch = plugin.getOptions()["type"].getValue()
        return ("repozer", RepozerSEA)


class RHSearchHtdocsRepozer(RHHtdocs):

    _local_path = os.path.join(os.path.dirname(indico.ext.search.repozer.__file__), "htdocs")
    _min_dir = 'repozer'
