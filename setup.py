from setuptools import setup 
#from setuptools import find_packages

if __name__ == '__main__':
    setup(
        name='repozer',
        version="0.9.4",
        description=("Repozer search plugin for Indico"), 
        author="Giorgio Pieretti",
        author_email = "pieretti@ictp.it", 
        #packages=find_packages(),
        packages = ['indico', 'indico.ext', 'indico.ext.search',
                'indico.ext.search.repozer',
                'indico.ext.search.repozer.tpls',
                'indico.ext.search.repozer.tpls.js',
                'indico.ext.search.repozer.htdocs',
                'indico.ext.search.repozer.htdocs.images'],
        namespace_packages=['indico.ext.search'],
        package_data={'indico.ext.search.repozer.tpls': ['*.tpl'],
                    'indico.ext.search.repozer.tpls.js': ['*.js'],
                  'indico.ext.search.repozer.htdocs.images': ['*.png']},
        install_requires = ['indico'],
        entry_points = {'indico.ext': ['search.repozer = indico.ext.search.repozer']}
    )
