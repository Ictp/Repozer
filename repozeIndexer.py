# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.

#from repoze.catalog.catalog import FileStorageCatalogFactory
#from repoze.catalog.catalog import ConnectionManager
try: from indico.core import db
except: from MaKaC.common import db

from MaKaC.plugins.base import PluginsHolder
from MaKaC.conference import ConferenceHolder
import MaKaC.common.info as info
from datetime import datetime
from pytz import timezone
import transaction
import Utils as ut
#import pyPdf

from repoze.catalog.catalog import Catalog as RCatalog
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.text import CatalogTextIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.document import DocumentMap
from indico.ext.search.repozer.options import confCatalog, contribCatalog, matCatalog
from indico.ext.search.repozer.converters import *
from repoze.catalog.query import *

class RepozerMaterial():
    
    def __init__(self, obj=None):
        self.__type__ = 'Material'
        self.id = 0
        self.title = ''
        self.conference = None
        self.session = None
        self.contribution = None
        self._owner = None
        self.description = None
        if obj:
            self._owner = obj.getOwner()
            locator = obj.getLocator()
            self.id = locator['materialId'] + '/' + locator['resId']
            self.ext = '.' + locator['fileExt']

            self.title = obj.name.decode('utf8')
            self.description = obj._content
            self.conference = self._owner.getConference()
            self.session = self._owner.getSession()
            self.contribution = self._owner.getContribution()
        
    def getTitle(self):
        return self.title.encode('utf8')
    
    def getId(self):
        return self.id
        
    def getConference(self):
        return self.conference
        
    def getSession(self):
        return self.session
        
    def getContribution(self):
        return self.contribution
    
    def getDescription(self):
        return self.description    
        


class RepozeCatalog():

    def __init__(self, catalogName=confCatalog):
        self.catalog = {}
        self.db = db.DBMgr.getInstance().getDBConnection()
        self.ch = ConferenceHolder()

        plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        self.iConf = plugin.getOptions()["indexConference"].getValue()
        self.iContrib = plugin.getOptions()["indexContribution"].getValue()
        self.iMat = plugin.getOptions()["indexMaterial"].getValue()

        # init all standard catalogs
        for cat in [confCatalog,contribCatalog,matCatalog]:
            if cat not in self.db.root():
                self.catalogName = cat
                self.init_catalog()        
        
        self.catalogName = catalogName

        # init customized catalog        
        if self.catalogName not in [confCatalog,contribCatalog,matCatalog] and self.catalogName not in self.db.root():
            self.init_catalog()
            
        self.catalog = self.db.root()[self.catalogName]

    
    def init_catalog(self):
        '''
        Create a repoze.catalog instance and specify
        indices of intereset
        '''        
        catalog = RCatalog()
        catalog.document_map = DocumentMap()                
        # set up indexes
        catalog['title'] = CatalogTextIndex('_get_title')
        catalog['titleSorter'] = CatalogFieldIndex('_get_sorter')
        catalog['collection'] = CatalogKeywordIndex('_get_collection')
        # Descriptions are converted to TEXT for indexing
        catalog['description'] = CatalogTextIndex('_get_description')
        catalog['startDate'] = CatalogFieldIndex('_get_startDate')
        catalog['endDate'] = CatalogFieldIndex('_get_endDate')
        catalog['modificationDate'] = CatalogFieldIndex('_get_modificationDate')
        catalog['fid'] = CatalogTextIndex('_get_fid')
        catalog['keywords'] = CatalogKeywordIndex('_get_keywordsList')
        catalog['category'] = CatalogKeywordIndex('_get_categoryList')
        # I define as Text because I would permit searched for part of names
        catalog['rolesVals'] = CatalogTextIndex('_get_roles')
        catalog['persons'] = CatalogTextIndex('_get_persons')

        self.db.root()[self.catalogName] = catalog
        self.catalog = self.db.root()[self.catalogName] 
        # commit the indexes
        transaction.commit()

        
    def indexConference(self, obj, catalog=None):
        if not(obj.hasAnyProtection()):        
            if not catalog: catalog = self.db.root()[confCatalog]
            fid = ut.getFid(obj)
            doc_id = catalog.document_map.new_docid()
            catalog.document_map.add(fid, doc_id) 

            obj._get_description = ut.getTextFromHtml(obj.getDescription()) 
            obj._get_title = obj.getTitle().decode('utf8','ignore')
            obj._get_sorter = obj._get_title.lower().replace(" ", "")[:10]
            obj._get_collection = [ut.get_type(obj, '')]
            obj._get_keywordsList = []     
            obj._get_categoryList = ut.getCatFid(obj)
            if hasattr(obj, '_keywords') and len(obj._keywords)>0: 
                obj._get_keywordsList = obj.getKeywords().replace('\r','').split('\n')
                 
            obj._get_roles = obj.getRolesVal()    
            obj._get_persons = ''
            if obj.getChairList(): 
                obj._get_persons = ut.getTextFromAvatar(obj.getChairList())
            
            obj._get_fid = fid
            obj._get_startDate = obj.getStartDate()
            obj._get_endDate = obj.getEndDate()       
            obj._get_modificationDate = obj.getModificationDate()        
            catalog.index_doc(doc_id, obj)    


    def indexContribution(self, obj, catalog=None):
        if not(obj.hasAnyProtection()):
            if not catalog: catalog = self.db.root()[contribCatalog]
            doc_id = catalog.document_map.new_docid()
            fid = ut.getFid(obj)
            confId, sessionId, talkId, materialId = fid.split("|")
            catalog.document_map.add(fid, doc_id) 
            localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
            nd = timezone(localTimezone).localize(datetime(1970,1,1, 0, 0)) # Set 1900/1/1 as None
            if not obj.startDate: obj.startDate = nd
            if not hasattr(obj, 'endDate'):
                obj.endDate = nd
            if hasattr(obj, 'duration') and obj.duration:
                obj.endDate = obj.startDate + obj.duration
        
            obj._get_categoryList = ut.getCatFid(self.ch.getById(confId))    
            obj._get_description = ut.getTextFromHtml(obj.getDescription()) 
            obj._get_title = obj.getTitle().decode('utf8','ignore')
            obj._get_sorter = obj._get_title.lower().replace(" ", "")[:10]
            obj._get_collection = [ut.get_type(obj, '')]
            obj._get_keywordsList = []     
            if hasattr(obj, '_keywords') and len(obj._keywords)>0: 
                 obj._get_keywordsList = obj.getKeywords().split('\n')
            obj._get_roles = '[]' 
            obj._get_persons = ''
            if obj.getSpeakerList(): 
                obj._get_persons = ut.getTextFromAvatar(obj.getSpeakerList())   
            
            obj._get_fid = fid
            obj._get_startDate = obj.getStartDate()
            obj._get_endDate = obj.getEndDate()
            obj._get_modificationDate = obj.getModificationDate()        
            #print "___Talk Title=",obj.getTitle()
            catalog.index_doc(doc_id, obj)


    def _indexMat(self, obj, catalog):
        doc_id = catalog.document_map.new_docid()
        robj = RepozerMaterial(obj)
        fid = ut.getFid(robj)
        confId, sessionId, talkId, materialId = fid.split("|")
        catalog.document_map.add(fid, doc_id) 
        robj._get_categoryList = ut.getCatFid(self.ch.getById(confId))
        robj._get_description = robj.getDescription()
        robj._get_title = robj.getTitle()
        robj._get_sorter = robj._get_title.lower().replace(" ", "")[:10]
        robj._get_collection = ['Material']
        robj._get_keywordsList = []     
        if hasattr(obj, '_keywords') and len(obj._keywords)>0: 
             robj._get_keywordsList = obj.getKeywords().split('\n')
        robj._get_roles = '[]'   
        robj._get_person = ''        
        robj._get_fid = fid
        localTimezone = info.HelperMaKaCInfo.getMaKaCInfoInstance().getTimezone()
        nd = timezone(localTimezone).localize(datetime(1970,1,1, 0, 0)) # Set 1900/1/1 as None
        robj._get_startDate = nd
        robj._get_endDate = nd 
        robj._get_modificationDate = nd        
        catalog.index_doc(doc_id, robj)         
        return   
                                
    def indexMaterial(self, res, catalog=None):
        if not catalog: catalog = self.db.root()[matCatalog]
        if not(res.isProtected()):
            try:
                ftype = res.getFileType().lower()
                fname = res.getFileName()
                fpath = res.getFilePath()
            except:
                ftype = None
            content = ''
            PDFc = pdf2txt()
            jod = jodconverter2txt()                
            if ftype in PDFc.av_ext: 
                # I do not use pyPDF because most of PDF are protected                
                PDFc.convert(fpath)
                content = PDFc.text
                res._content = content
                #print ".... indexing Material ",fpath, "___content=",content[:50]
                self._indexMat(res, catalog)
            if ftype in jod.av_ext:
                jod.convert(fpath, ftype)
                content = jod.text
                res._content = content
                #print ".... indexing Material ",fpath, "___content=",content[:50]
                self._indexMat(res, catalog)
            PDFc = None
            jod = None
        return
    
                
    def fullIndex(self, obj):   
        fid = ut.getFid(obj)
        confId, sessionId, talkId, materialId = fid.split("|")
        conf = self.ch.getById(confId) 

        if self.iConf:
            catalog = self.db.root()[confCatalog]
            self.indexConference(conf, catalog)
            if self.iMat:            
                for mat in conf.getAllMaterialList(): # Index Material inside Conference
                    for res in mat.getResourceList():
                        self.indexMaterial(res)

        if self.iContrib:
            for talk in conf.getContributionList():
                catalog = self.db.root()[contribCatalog]
                self.indexContribution(talk, catalog)
                if self.iMat:   
                    for mat in talk.getAllMaterialList(): # Index Material inside Contributions
                        for res in mat.getResourceList():
                            self.indexMaterial(res)
                             
        transaction.commit() 

    
    def indexObject(self, obj):

        cname = obj.__class__.__name__
        if cname == 'Conference' and self.iConf:
            objExist = True
            try: o = self.ch.getById(obj.getId())
            except: objExist = False
            # if obj has not been DELETED:
            if objExist:
                self.indexConference(obj)

        if cname == 'Contribution' and self.iContrib:
            self.indexContribution(obj)

        if cname == 'LocalFile' and self.iMat:
            try:
                self.indexMaterial(obj)
            except:
                pass
        
    
    def unindexObject(self, obj, recursive=False):
        
        fid = ut.getFid(obj)
        if fid == '|||': return
        conf = None
        cname = obj.__class__.__name__
        useCatalog = None

        if cname == 'Conference' and self.iConf:
            useCatalog = confCatalog
            confId, sessionId, talkId, materialId = fid.split("|")  

            cat = self.db.root()[confCatalog]
            (hits, res) = cat.query(Eq('fid',fid))
            for doc_id in res:
                #print "__unindex fid=",fid,"__TITLE=", obj.getTitle()
                cat.unindex_doc(doc_id) 

            if recursive:
                # also remove inner objects
                for cat in [self.db.root()[contribCatalog],self.db.root()[matCatalog]]:
                    (hits, res) = cat.query(Eq('fid',confId+'|*'))
                    for doc_id in res:
                        cat.unindex_doc(doc_id)

        if cname == 'Contribution' and self.iContrib:
            useCatalog = contribCatalog
            # Remove Contrib:
            cat = self.db.root()[contribCatalog]
            (hits, res) = cat.query(Eq('fid',fid))
            for doc_id in res:
                cat.unindex_doc(doc_id) 
                if recursive:
                    # also remove inner objects
                    cat = self.db.root()[matCatalog]
                    (hits, res) = cat.query(Eq('fid',fid+'*'))
                    for doc_id in res:
                        cat.unindex_doc(doc_id) 

        if cname == 'LocalFile' and self.iMat:                          
            cat = self.db.root()[matCatalog]
            (hits, res) = cat.query(Eq('fid',fid))
            for doc_id in res:
                cat.unindex_doc(doc_id)
            
  

        
    def closeConnection(self):
        #transaction.commit()              
        #self.factory.db.close()
        #self.manager.commit()        
        #self.manager.close() 
        return

    def openConnection(self):
        #plugin = PluginsHolder().getPluginType('search').getPlugin("repozer")
        #DBpath = plugin.getOptions()["DBpath"].getValue()
        #self.factory = FileStorageCatalogFactory(DBpath,'repoze_catalog')
        #self.manager = ConnectionManager()
        #self.catalog = self.factory(self.manager)
        return
