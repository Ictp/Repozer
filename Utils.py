# -*- coding: utf-8 -*-
##
##
## This file is added for Indexing Indico's contents with repoze.catalog
## Copyright (C) 2013 Ictp.
from lxml import html

def getRolesValues(conf):
    # convert roles to list of values only
    vals = []
    if hasattr(conf,'_roles'):
        sroles = str(conf._roles).replace('false','False').replace('true','True')
        if sroles != '[]':
            lroles = eval(sroles)
            vals = []
            for r in lroles:
                child = r['child']                
                for c in child:
                    if 'familyName' in c:
                        vals.append(c['familyName'])
                    if 'firstName' in c:
                        vals.append(c['firstName'])
    return ','.join(vals)


def getTextFromHtml(txt):
    s = ''
    if txt: 
        try:
            s = html.fromstring(txt.decode('utf8','ignore')).text_content()
            # Change this if you need different encoding
            s = s.encode('ascii','ignore')
        except: 
            s = txt
    return s