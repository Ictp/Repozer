from setuptools import setup, find_packages
if __name__ == '__main__':
    setup(
        name='repozer',
        version="1.0.1",
        description="Indico search plugin",
        author="Giorgio Pieretti",
        packages=find_packages(),
        include_package_data=True,
        #install_requires=["repoze.catalog",],
        package_dir={'repozer': 'repozer'},
        entry_points="""
            [indico.ext]
            search.repozer = indico.ext.search.repozer
        """
    )