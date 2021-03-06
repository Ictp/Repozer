Repozer
=======

Indico external module for integrated search engine based on repoze.catalog module


WHAT IS REPOZER 
---------------

Repozer is an integration of repoze.catalog ( http://docs.repoze.org/catalog/ )
into Indico as a search plug-in.
Indico comes with few integrated search functionality.
Repozer gives you the ability to search inside Events directly in Indico, without external tools.
Searching with repoze.catalog is very easy and powerful, if you need some customized query just
take a look at: http://docs.repoze.org/catalog/usage.html#searching




INSTALLATION
------------


### PRESEQUISITES:

We strongly suggest you to install your Indico instance from SOURCE: 
    http://indico-software.org/wiki/Dev/GettingStarted
Otherwise, you will have to change your source files in 
    /<Indico path>/lib/python2.6/site-packages    
*Indico v. 1.2 is REQUIRED*
    


### STEP 1: Install Repoze staff



- Go to "<Indico path>/src/indico/ext/search/" and clone the repo (*or you can clone it wherever you want, then put a sym link to that path*):

```
    git clone https://github.com/Ictp/Repozer.git repozer
```

*This should also install repoze.catalog . If it fails, you can do it manually: pip install repoze.catalog*


- Save and from shell in <Indico path>/src/indico/ext/search/repozer:

```
    $ python setup.py install
```
    

    
### STEP 2: Configure and create Catalog

- Start Indico    
- Enter Admin web interface, Plugins, Reload All Manually
- If you get the "ModuleLoadException: Impossible to load indico.ext.search.repozer" error, it means that you need a symbolic link to your repozer src folder. 

Eg: /usr/lib/python2.6/site-packages/indico-1.2-py2.6.egg/indico/ext/search/$ ln -s /opt/indico/src/indico/ext/search/repozer repozer 
- Enable Search plugin, Repozer, set default Sea = Repozer and Save Settings, ENABLE/DISABLE Indexing properties!
- Via shell, go to "<Indico path>/src/indico/ext/search/repozer/manage" and type:

```
    $ python createRepozeCatalog.py
```

this will create the repozecatalog inside your Data.fs (you should see percentage numbers)
- It could take a long time. At the end it will pack your DB.
- For better performances, we use 3 catalogs: for Conferences (rc_Event), Contributions (rc_Contribution) and Materials (rc_Material). If you prefere using the same catalog for all Items take a look at options.py


**Now your search engine is up-n-running!**



MATERIAL INDEXING!
------------------

With Repozer > 0.9.2 Materials are now indexable!!! You will be able to search for:
'pdf','doc','docx','odt','rtf','wpd','txt','html','xlsx','ppt','pptx','xls','ods','odp','sxc','sxw','csv','sxi'

... but you have to follow some additional STEPS:


- INSTALL Poppler and OpenOffice/LibreOffice, with headless pkg:
    - - yum install poppler
    - - yum install poppler-utils
    - - yum install libreoffice
    - - yum install libreoffice-headless 
    
- UNCOMMENT line 13 in tpls/SearchResult.tpl : to make Material visible in the 'search in' combo

- Enable Material Indexing in Search PLUGIN properties (disabled by default)

- Add some code to MaKaC/conference.py to notify creation/editing/deleting od Materials:

@ line 11368, (Resource class, notifyModification method) right after:  parent.setModificationDate()

```
            # added for Indexing
            self._notify('infoChanged')
```

@ line 11452, (Resource class, delete method) right after:  if self._owner is not None:

```
            # notifiy deleting for indexing
            self._notify('deleted', self._owner)
```


- START OpenOffice/LibreOffice service: 

```
    $ soffice --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard 
```

- DONE! Now you can re-run createRepozeCatalog.py for indexing all contents WITH Materials!

Search also inside Materials WORKS with different charsets.



BEWARE!
-------

There are some things that you should notice:
- Results pagination has been disabled and results are limited
    (you can change this behaviour by yourself by looking into code)


HTTP_API.PY
-----------

You can also use Repozer with http_api for letting thirdy-party software to 
make queries to Indico and receive XML/JSON (form JSON use 'search.json') output.
To understand it better, just take a look at http_api.py 
E.g. you can make a call like this:

```
http://<Indico URL>/export/conference/search.xml?start_date=2013/01/01&keywords=Condensed Matter and Statistical Physics,Computational Physics in Condensed Matter
```

Usable Parameters are:

- start_date
- end_date   
- today (shows Conferences running, alternative for start/end_date)
- keywords
- category

But you can easily edit the code to search for other fields, like in implementation.py
To get richer Events data, you can change default DETAILS.
E.g.:

```
http://<Indico URL>/export/conference/search.json?detail=contributions&today=2013/04/10
```



**Enjoy! :)**

