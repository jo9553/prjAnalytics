#import setuptools
#from distutils.core import setup
from setuptools import setup

setup(
    name='StockCrisisDateWeb',
    version='0.1',
    author='Joyce Leung',
    author_email="doublefin576@gmail.com",
    description="Web version for collecting date of stock crisis",
    license="GPLv3+",
    packages=["StockCrisisDateWeb"],
    url="https://github.com/jo9553/prjStock",
    install_requires=[
        'pandas',
        'tables',  # Needed by pandas.HDFStorei
        'h5py',
        'lxml',
        'html5lib'
    ],
    entry_points='''
        [console_scripts]
        StockCrisisDateWeb=StockCrisisDateWeb.stockcrisisdateweb:readHTML
    '''
)
