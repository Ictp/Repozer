Repozer
=======

Indico external module for integrated search engine based on repoze.catalog module


WHAT IS REPOZER 
---------------

Repozer is an integration of repoze.catalog ( http://docs.repoze.org/catalog/ )
into Indico as a search plug-in.
Indico comes with few integrated search functionality (search for Categories, not Events).
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

    


### STEP 1: Install Repoze staff

- Install Repoze in your Indico instance:

```
    $ pip install repoze.catalog
```

- go to "<Indico path>/src/indico/ext/search/" and do:

```
    git clone https://github.com/Ictp/Repozer.git repozer
```

- Edit "<Indico path>/src/setup.py", add @566 (right below "search.invenio = indico.ext.search.invenio")

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
- Enable Search plugin, Repozer, set default Sea = Repozer and Save Settings
- Via shell, go to "<Indico path>/src/indico/ext/search/repozer/manage" and type:

```
    $ python createRepozeCatalog.py
```

this will create the repozecatalog inside your Data.fs (you should see percentage numbers)
- It could take a long time. At the end it will pack your DB.


**Now your search engine is up-n-running!**



MATERIAL INDEXING!
------------------

With Repozer 0.9.2 Materials are now indexable!!! You will be able to search for:
'pdf','doc','docx','odt','rtf','wpd','txt','html','xlsx','ppt','pptx','xls','ods','odp','sxc','sxw','csv','sxi'

... but you have to follow some additional STEPS:


- INSTALL Poppler and OpenOffice/LibreOffice, with headless pkg:
- -    yum install poppler
- -    yum install libreoffice
- -    yum install libreoffice-headless 
    
- UNCOMMENT line 13 in tpls/SearchResult.tpl : to make Material visible in the 'search in' combo

- EDIT options.py and comment/uncomment as specified

- START OpenOffice/LibreOffice service: 

```
    $ soffice --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard 
```

- DONE! Now you can re-run createRepozeCatalog.py for indexing all your Materials!

- IMPORTANT: Right now, I do not have found an hook to the add/remove/edit Material event, 
so if you add/remove/edit Materials the Repozer Catalog wont know that! :(
The suggeste way to solve the issue is a CRONJOB that, once a day for example, checks for edited Conferences and
re-index them. I've prepared a python script that achieve this: manage/updateMaterials.py
So, last suggested STEP:

- PUT THIS in your cronjob:

```
    0 2 * * * /usr/bin/python /opt/indico/src/indico/ext/search/repozer/manage/updateMaterials.py 
```

Search also inside Materials WORKS now with different charsets!!!



BEWARE!
-------

There are some things that you should notice:
- Results pagination has been disabled and results are limited to 5000 
    (you can change this behaviour by yourself by looking into code)
- You can add/edit indexing by editing repozeIndexer.py and createRepozeCatalog.py


HTTP_API.PY
-----------

You can also use Repozer with http_api for letting thirdy-party software to 
make queries to Indico and receive XML/JSON (form JSON use 'search.json') output.
To understand it better, just take a look at http_api.py 
E.g. you can make a call like this:

```
http://<Indico URL>/indico/export/conference/search.xml?start_date=2013/01/01&keywords=Condensed Matter and Statistical Physics,Computational Physics in Condensed Matter
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
http://<Indico URL>/indico/export/conference/search.json?detail=contributions&today=2013/04/10
```



**Enjoy! :)**

