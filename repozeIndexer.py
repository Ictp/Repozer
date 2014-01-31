# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.

from repoze.catalog.catalog import FileStorageCatalogFactory
from repoze.catalog.catalog import ConnectionManager
from MaKaC.plugins.base import PluginsHolder
from MaKaC.conference import ConferenceHolder
import MaKaC.common.info as info
from datetime import datetime
from pytz import timezone
import transaction
import Utils as ut
import pyPdf

from indico.ext.search.repozer.options import typesToIndicize

class RepozeCatalog():

    def __init__(self):
        self.catalog = {}
        self.factory = None
        self.manager = None
        self.openConnection()
        pass
    
    
    def indicizeConference(self, obj, catalog=None):
        if not catalog: catalog = self.catalog
        fid = ut.getFid(obj)
        doc_id = catalog.document_map.new_docid()
        catalog.document_map.add(fid, doc_id) 

        obj._get_description = ut.getTextFromHtml(obj.getDescription()) 
        obj._get_sorter = str(obj.getTitle()).lower().replace(" ", "")[:10]
        obj._get_collection = [ut.get_type(obj, '')]
        obj._get_keywordsList = []     
        if hasattr(obj, '_keywords') and len(obj._keywords)>0: 
             obj._get_keywordsList = obj.getKeywords().split('\n')
        obj._get_roles = ut.getRolesValues(obj)    
        obj._get_person = ''
        obj._get_title = obj.getTitle()
        obj._get_startDate = obj.getStartDate()
        obj._get_endDate = obj.getEndDate()        
        
        catalog.index_doc(doc_id, obj)    


    def indicizeContribution(self, obj, catalog=None):
        if not catalog: catalog = self.catalog
        doc_id = catalog.document_map.new_docid()
        fid = ut.getFid(obj)
        catalog.document_map.add(fid, doc_id) 
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        nd = timezone(localTimezone).localize(datetime(1970,1,1, 0, 0)) # Set 1900/1/1 as None
        if not obj.startDate: obj.startDate = nd
        if not hasattr(obj, 'endDate'):
            obj.endDate = nd
        if hasattr(obj, 'duration') and obj.duration:
            obj.endDate = obj.startDate + obj.duration
            
        obj._get_description = ut.getTextFromHtml(obj.getDescription()) 
        obj._get_sorter = str(obj.getTitle()).lower().replace(" ", "")[:10]
        obj._get_collection = [ut.get_type(obj, '')]
        obj._get_keywordsList = []     
        if hasattr(obj, '_keywords') and len(obj._keywords)>0: 
             obj._get_keywordsList = obj.getKeywords().split('\n')
        obj._get_roles = ut.getRolesValues(obj)    
        data = []
        for s in obj.getSpeakerList():
            name = s.getValues()['familyName']
            if hasattr(s.getValues(), 'firstName'): name += ' ' + s.getValues()['firstName']
            if hasattr(s.getValues(), 'affiliation'): name += ' ' + s.getValues()['affiliation']
            data.append(name)
        if data: obj._get_person = str(' '.join(data))
        else: obj._get_person = ''               
        obj._get_title = obj.getTitle()
        obj._get_startDate = obj.getStartDate()
        obj._get_endDate = obj.getEndDate()
            
        catalog.index_doc(doc_id, obj)


    def indicizeMaterial(self, obj, catalog=None):
        if not catalog: catalog = self.catalog
        doc_id = catalog.document_map.new_docid()
        fid = ut.getFid(obj)
        catalog.document_map.add(fid, doc_id) 
        
        obj._get_description = ut.getTextFromHtml(obj.getDescription()) 
        obj._get_description += obj._content
        obj._get_sorter = str(obj.getTitle()).lower().replace(" ", "")[:10]
        obj._get_collection = [ut.get_type(obj, '')]
        obj._get_keywordsList = []     
        if hasattr(obj, '_keywords') and len(obj._keywords)>0: 
             obj._get_keywordsList = obj.getKeywords().split('\n')
        obj._get_roles = ''    
        obj._get_person = ''
        obj._get_title = obj.getTitle()
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        nd = timezone(localTimezone).localize(datetime(1970,1,1, 0, 0)) # Set 1900/1/1 as None
        obj._get_startDate = nd
        obj._get_endDate = nd       
        print "FID=",fid,"_____DESCR=",obj._get_description[:100]      
        catalog.index_doc(doc_id, obj)    
                
                
                
                
    def index(self, conf):   
        if 'Conference' in typesToIndicize:
            self.indicizeConference(conf)

        if 'Contribution' in typesToIndicize:
            for talk in conf.getContributionList():
                talk._catName = conf._catName                   
                self.indicizeContribution(talk)

        if 'Material' in typesToIndicize:
            for mat in conf.getAllMaterialList():
                print "qui",vars(mat)
                mat._catName = conf._catName                
                for res in mat.getResourceList():
                    print "res..."
                    ftype = res.getFileType()
                    fname = res.getFileName()
                    fpath = res.getFilePath()
                    content = ''
                    if ftype == 'PDF':                            
                        try:
                            pdf = pyPdf.PdfFileReader(open(fpath, "rb"))
                            for page in pdf.pages:
                                content += ' '+page.extractText()                            
                        except:
                            # something has gone wrong
                            print "ERROR indexing material:",ut.getFid(mat)
                            pass
                        mat._content = content
                        print "indexing material:",fpath    
                        self.indicizeMaterial(mat)

    def _unindexFid(self, fid):
        try:
            doc_id = self.catalog.document_map.docid_for_address(fid)
            self.catalog.unindex_doc(doc_id)
        except:
            pass

        
    def unindex(self, conf):    
        print "UNINDEX"
        if 'Material' in typesToIndicize:
            for mat in conf.getAllMaterialList():
                for obj in mat.getResourceList():
                    self._unindexFid(ut.getFid(obj))
        if 'Contribution' in typesToIndicize:
            for obj in conf.getContributionList():
                self._unindexFid(ut.getFid(obj))
        if 'Conference' in typesToIndicize:
            self._unindexFid(ut.getFid(conf))

        
    def reindex(self, c):
        fid = ut.getFid(c)
        confId, sessionId, talkId, materialId = fid.split("|")
        print "REINDEX",fid
        # Check if conference still exist
        ch = ConferenceHolder()        
        cc = None
        # THIS CAN BE OPTIMIZED    
        try: cc = ch.getById(confId)
        except: pass            
        if cc:
            self.unindex(cc)
            self.index(cc)

        
    def closeConnection(self):
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
