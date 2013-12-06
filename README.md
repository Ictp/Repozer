Repozer
=======

Indico external module for integrated search engine based on repoze.catalog module


WHAT IS REPOZER 
---------------

Repozer is an integration of repoze.catalog ( http://docs.repoze.org/catalog/ )
into Indico as a search plug-in.
Indico comes with few integrated search functionality (search for Categories, not Events).
Repozer gives you the ability to search inside Events directly in Indico, without any external tools.
Searching with repoze.catalog is very easy and powerful, if you need some customized query just
take a look at: http://docs.repoze.org/catalog/usage.html#searching




INSTALLATION
------------

Unfortunatly the installation procedure is not click-n-go, but you do it just once.

### PRESEQUISITES:

We strongly suggest you to install your Indico instance from SOURCE: 
    http://indico-software.org/wiki/Dev/GettingStarted
Otherwise, you will have to change your source files in 
    /<Indico path>/lib/python2.6/site-packages    

    


### STEP 1: Install Repoze staff

- Install Repoze in your Indico instance:

```
    $ pip install repoze.catalog
```

- go to "<Indico path>/src/indico/ext/search/" and do:

```
    git clone https://github.com/Ictp/Repozer.git repozer
```

- Edit "<Indico path>/src/setup.py", add @547 (right below "search.invenio = indico.ext.search.invenio")

```
    search.repozer = indico.ext.search.repozer
```

- Save and from shell in <Indico path>/src/:

```
    $ python setup.py develop_config
```
    

    
### STEP 2: Configure and create Catalog

- Start Indico    
- Enter Admin web interface, Plugins
- Enable Search plugin, Repozer, set default Sea = Repozer
- Set Repozer DB path (*** CHECK IT!!! ***) and Save Settings
- Via shell, go to "<Indico path>/src/indico/ext/search/repozer/manage" and type:

```
    $ python createRepozeCatalog.py
```

this will create the inidico_catalog.fs (you should see percentage numbers)
- chown (apache:apache or whatever) the indico_catalog.fs and related files



**Now your search engine is up-n-running!**

To make it updated with Events editing you can:

1) put in CRON the createRepozeCatalog.py
    - this will recreate the whole catalog everytime, but it should not take too long

*OR BETTER*

2) go below to OPTIONAL - STEP 3
    - this will make you edit a couple of source files so when an Event change the Repoze Catalog
    will change accordingly and will always be updated in realtime.



### OPTIONAL - STEP 3: Update Indico source for Indexing

- edit "MaKaC/webinterface/rh/categoryDisplay.py"
    
    search for "class RHConferencePerformCreation"
    in method "def _createEvent(self, params):"
    just BEFORE "return c", add:

```    
        from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
        rc = RepozeCatalog()
        rc.index(c)          
```
- edit "MaKaC/common/indexes.py"

    search for "class CategoryIndex"
    in method "unindexConf(self, conf):"
    at the END add:

```    
        from indico.ext.search.repozer.repozeIndexer import RepozeCatalog
        rc = RepozeCatalog()
        rc.unindex(conf)
```




BEWARE!
-------

There are some things that you should notice:
- Results pagination has been disabled and results are limited to 5000 
    (you can change this behaviour by yourself by looking into code)
- Search is inside Events, not Contributions (right now, to make it faster... in the future we will let you choose)
- You can add/edit indexing by editing repozeIndexer.py and createRepozeCatalog.py


### SPECIFIC CUSTOMIZATION:

Because of Repozer has been developed by Ictp, there are few customization you should change 
according to your company needs. Take a look inside files of Repozer package: 
- implementation.py : lines 328 and 355
- tpls/SearchBoxBase.tpl : line 34
- tpls/SearchResultBase.tpl : line 55







HTTP_API.PY
-----------

You can also use Repozer with http_api for letting thirdy-party software to 
make queries to Indico and receive XML/JSON output.
To understand it better, just take a look at http_api.py 
E.g. you can make a call like this:

```
http://<Indico URL>/indico/export/conference/search.xml?start_date=2013/01/01&keywords=Analysis,Physics
```

Usable Parameters are:

- start_date
- end_date   
- keywords
- category

But you can easily edit the code to search for other fields, like in implementation.py
Enjoy! :)

