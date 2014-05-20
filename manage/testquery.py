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

try: from indico.core import db
except: from MaKaC.common import db

from MaKaC.conference import CategoryManager, ConferenceHolder
from MaKaC.plugins.base import PluginsHolder
from indico.ext.search.repozer import Utils as ut
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *
import transaction


db.DBMgr.getInstance().startRequest()
rc = RepozeCatalog()
    
    

if __name__ == '__main__':     
    testo = '*Retribuzione*'
    #(hits,results) =  rc.catalog.query((Eq('description', testo) | Eq('title', testo)) & Any('collection', 'Material')    )  
    (hits,results) =  rc.catalog.query(Eq('description', testo) | Eq('title', testo) )  
    results = [rc.catalog.document_map.address_for_docid(result) for result in results] 
    print hits, results
    db.DBMgr.getInstance().endRequest()
    
