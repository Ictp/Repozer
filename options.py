# -*- coding: utf-8 -*-
##
##
## This file is part of Indico
## Copyright (C) 2002 - 2013 European Organization for Nuclear Research (CERN)
##
## Indico is free software: you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico.  If not, see <http://www.gnu.org/licenses/>.
from MaKaC.i18n import _

from indico.core.config import Config


# This is for external DB
#globalOptions = [
#    ("DBpath", {"description": "Repozer DB path",
#                  "type": str,
#                  "defaultValue": "/opt/indico/db/repoze_catalog.fs",
#                  "editable": True,
#                  "visible": True}),
#]
globalOptions = [
    ("liveUpdate", {"description" : "Repozer will index contents automatically",
               "type": bool,
               "defaultValue": True,
               "editable": True,
               "visible": True} ),
]

# By default Material indexing is disabled
typesToIndex = ['Conference','Contribution']
#typesToIndex = ['Conference']

availableCatalogs = ['rc_Event','rc_Contribution','rc_Material']
