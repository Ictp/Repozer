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
from indico.ext.search.repozer.options import typesToIndex
from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
from repoze.catalog.query import *
import transaction
from datetime import datetime


db.DBMgr.getInstance().startRequest()
rc = RepozeCatalog()

def buildCatalog():
    rc.init_catalog() # Forces index rebuild
    cm = CategoryManager()
    ch = ConferenceHolder()
    totnum = len(ch.getValuesToList())
    curnum = 0
    curper = 0
    
    startFrom = 1889
    
    print "Events found:", totnum
        
    for c in ch.getValuesToList():
        if curnum >= startFrom:
            #if c and c.getId() == 'a12226':    
            print curnum,".......confid=",c.getId()
            
            
            # CUSTOM CASES FOR ICTP
#             if c.getRoles().find('\r\n') != -1:
#                 c.setRoles(c.getRoles().replace('\r\n',''))
#                 transaction.commit()
#             if c.getId() == 'a0344':
#                 c.setRoles('[{"id":2,"value":"Director(s)","editable":False,"child":[{"id":0,"familyName":"A. Simis"}, {"id":1,"familyName":"N.V. Trung and G. Valla"}]}, {"id":5,"value":"Director(s) & organizer(s)","editable":False,"child":[{"id":0,"familyName":"Scientific Committee: C. Huneke"}, {"id":1,"familyName":"A. Simis"}, {"id":2,"familyName":"B. Sturmfels"}, {"id":3,"familyName":"N.V. Trung"}, {"id":4,"familyName":"G. Valla and J. Verma"}]}, {"id":4,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"C. Huneke"}, {"id":1,"familyName":"A. Simis"}, {"id":2,"familyName":"N.V. Trung"}, {"id":3,"familyName":"G. Valla and J. Verma"}]}, {"id":1,"value":"Local organizer(s)","editable":False,"child":[{"id":0,"familyName":"Ramadas T. Ramakrishnan"}]}, {"id":1,"value":"Laboratories","editable":False,"child":[{"id":0,"familyName":"no"}]}, {"id":1,"value":"Secretary","editable":False,"child":[{"id":0,"familyName":"A. Bergamo"}]}, {"id":5,"value":"Cosponsor(s)","editable":False,"child":[{"id":0,"familyName":"Research Project -Commutative and Computer Algebra-"}, {"id":1,"familyName":"MIUR"}, {"id":2,"familyName":"and Department of Mathematics"}, {"id":3,"familyName":"University of Genoa - Italy"}]}]')
#                 transaction.commit()
#             if c.getId() == 'a0432':
#                 c.setRoles('[{"id":2,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"Liceo Ginnasio Statale Francesco Petrarca"}, {"id":1,"familyName":"Trieste; contact: Prof. Marina Mai"}]}]')
#                 transaction.commit()
#             if c.getId() == 'a07198':
#                 c.setRoles('[{"id":4,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"Prof. G.F. Panza (ICTP - ESP-SAND)"}, {"id":1,"familyName":"Prof. F.M. Mazzolani (University of Naples Federico II)"}, {"id":2,"familyName":"Ing. M. Indirli (ENEA-Bologna)."}]}, {"id":1,"value":"Secretary","editable":False,"child":[{"id":0,"familyName":"G. De Meo"}]}]')
#                 transaction.commit()    
#             if c.getId() == 'a08192':
#                 c.setRoles('[{"id":7,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"Directors: S. Cozzini"}, {"id":1,"familyName":"P. Giannozzi"}, {"id":2,"familyName":"E. Menendez-Proupin"}, {"id":3,"familyName":"W. Orellana"}, {"id":4,"familyName":"S. ScandoloCo-Organizing Institutions: Universidad Andrés Bello (UNAB)"}, {"id":5,"familyName":"Santiago"}, {"id":6,"familyName":"Chile;Project Anillo ACT/24/2006 - Universidad de Chile -Computer Simulation Lab in Nanobio Systems- INFM - DEMOCRITOS  National Simulation Center"}]}, {"id":1,"value":"Secretary","editable":False,"child":[{"id":0,"familyName":"M. Poropat"}]}, {"id":3,"value":"Collaborations","editable":False,"child":[{"id":0,"familyName":"Universidad Andrés Bello (UNAB)"}, {"id":1,"familyName":"Santiago"}, {"id":2,"familyName":"Chile and Project Anillo ACT/24/2006 - Universidad de Chile -Computer Simulation Lab in Nanobio Systems-"}]}, {"id":2,"value":"Cosponsor(s)","editable":False,"child":[{"id":0,"familyName":"Comisión Nacional de Investigación Científica y Tecnológica (CONICYT)"}, {"id":1,"familyName":"Programa Bicentenario de Ciencia y Tecnología"}]}]')
#                 transaction.commit()     
#             if c.getId() == 'a09174':
#                 c.setRoles('[{"id":4,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"Directors:  A. Belehaki"}, {"id":1,"familyName":"M. Messerotti"}, {"id":2,"familyName":"G.  Lapenta"}, {"id":3,"familyName":"S. Radicella"}]}, {"id":1,"value":"Laboratories","editable":False,"child":[{"id":0,"familyName":"AGH Infolab (afternoons)"}]}, {"id":1,"value":"Secretary","editable":False,"child":[{"id":0,"familyName":"S. Radosic"}]}, {"id":5,"value":"Cosponsor(s)","editable":False,"child":[{"id":0,"familyName":"EC COST Action ES0803 -Developing Products and Services for Space Weather in Europe-"}, {"id":1,"familyName":"EC FP7 Project SOTERIA -SOLar-TERrestrial Investigations and Archives-"}, {"id":2,"familyName":"National Institute for Astrophysics (INAF) European Space Agency (ESA)"}]}]')
#                 transaction.commit()     
#             if c.getId() == 'a09223':
#                 c.setRoles('[{"id":5,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"M. Bianchi (University of Rome -Tor Vergata-)"}, {"id":1,"familyName":"S. Ferrara (CERN & INFN)"}, {"id":2,"familyName":"E. Kiritsis (University of Crete)"}, {"id":3,"familyName":"K. Narain (ICTP)"}, {"id":4,"familyName":"S. Randjbar-Daemi (ICTP) and A. Sen (HRI)"}]}, {"id":1,"value":"Secretary","editable":False,"child":[{"id":0,"familyName":"R. Sain"}]}, {"id":1,"value":"Cosponsor(s)","editable":False,"child":[{"id":0,"familyName":"the Asia Pacific Center for Theoretical Physics (APCTP) & the Italian Institute for Nuclear Physics (INFN)"}]}]')
#                 transaction.commit()     
#             if c.getId() == 'a0924':
#                 c.setRoles('[{"id":2,"value":"Organizer(s)","editable":False,"child":[{"id":0,"familyName":"Liceo Ginnasio Statale -F. Petrarca- e Liceo -G. Galilei-"}, {"id":1,"familyName":"Trieste; contacts: Prof. Philip Tarsia and Ms. Renata Grill (Liceo Galilei)."}]}, {"id":1,"value":"Laboratories","editable":False,"child":[{"id":0,"familyName":"LB LAB"}]}]')
#                 transaction.commit()     

                
            rc.index(c) 
            transaction.commit()
        curnum += 1

        per = int(float(curnum)/float(totnum)*100)
        if per != curper:
            curper = per
            print "______________"+str(per)+"%"
        
    # Pack it when finished
    print "Packing...."
    db.DBMgr.getInstance().pack()
    print "Done."
    
    

if __name__ == '__main__':  
    migrStartTime = str(datetime.now())
    buildCatalog()
    migrEndTime = str(datetime.now())   
    print "Indexing started at: ",migrStartTime
    print "Indexing ended at: ",migrEndTime  
    db.DBMgr.getInstance().endRequest()
    
