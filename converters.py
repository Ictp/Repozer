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

import os, tempfile
from subprocess import Popen
from indico.ext.search.repozer import Utils as ut
#import shutil

""" 
To be able to use jodconverter don't forget to start soffice service: 
soffice --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard 
"""

class commonConverter():

    def getContent(self, fpath):
        txt = ''
        f = None
        try: f = open(fpath, 'r')
        except: pass
        if f:    
            txt = f.read()
            f.close()
        return txt.replace("\r\n", " ").replace("\n", " ").decode(self.output_encoding,'ignore')
                
                
class pdf2txt(commonConverter):
    
    def __init__(self):
        self.output_encoding = 'UTF-8'    
        self.binary = "pdftotext"
        self.binaryArgs = "-nopgbrk -enc " +  self.output_encoding
        self.av_ext = ['pdf'] 
        self.text = ''   
        self.tempdirpath = ''
        self.suffix = '.txt'
    
    def convert(self, fpath):
        self.tempdirpath = tempfile.mkdtemp()
        sourcename = fpath.split('/')[-1]
        destpath = self.tempdirpath + '/' + sourcename + self.suffix
        self.text = self.invokeCommand(fpath, destpath)        
        return
 
    def invokeCommand(self, fpath, destpath):
        txt = ''
        cmd = 'cd "%s" && %s %s %s %s' % (self.tempdirpath, self.binary, self.binaryArgs, fpath, destpath)        
        #print "COMMAND=",cmd
        #p = Popen(cmd, shell = True)
        #sts = os.waitpid(p.pid, 0)
        p = os.popen(cmd)
        p.close()
        txt = ''
        txt = self.getContent(destpath)
        p = os.popen("rm -rf "+self.tempdirpath)
        p.close()                
        return txt
        



class jodconverter2txt(commonConverter):
    
    def __init__(self):
        self.output_encoding = 'UTF-8'    
        self.binary = "java"
        self.binaryArgs = "-jar jodconverter/lib/jodconverter-cli-2.2.2.jar"
        self.av_ext_txt = ['doc','docx','odt','rtf','wpd','txt','html',] 
        self.av_ext_html = ['xlsx','ppt','pptx','xls','ods','odp','sxc','sxw','csv','sxi']
        self.av_ext = self.av_ext_txt + self.av_ext_html
        self.text = ''
        self.suffix = '.txt'
        self.tempdirpath = ''

    def convert(self, fpath, ftype):
        if ftype in self.av_ext_html:
            self.suffix = '.html'    
        self.tempdirpath = tempfile.mkdtemp()
        sourcename = fpath.split('/')[-1]
        destpath = self.tempdirpath + '/' + sourcename + self.suffix
        self.text = self.invokeCommand(fpath, destpath)             
        return
    
  
        
    def invokeCommand(self, fpath, destpath):
        cmd = '%s %s %s %s' % (self.binary, self.binaryArgs, fpath, destpath)
        #print "COMMAND=",cmd
        #p = Popen(cmd, shell = True)
        #sts = os.waitpid(p.pid, 0)
        p = os.popen(cmd)
        p.close()
        txt = ''
        if self.suffix == '.html':
            for filename in os.listdir(self.tempdirpath):
                if filename.endswith(".html"):
                    txt += ut.getTextFromHtml(self.getContent(self.tempdirpath + '/' + filename))
        else:
            txt = self.getContent(destpath)
        p = os.popen("rm -rf "+self.tempdirpath)
        p.close()
        return txt

