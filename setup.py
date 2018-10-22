"""Setup configuration for Offline Assimilation package.

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open  # 2.7 only
import glob

# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Ofline Assimilation',
    version='0.0.1',
    description='Improving reanalysis with offline assimilation',

    # From README - see above
    long_description=long_description,
    #long_description_content_type='text/x-rst',

    url='https://brohan.org/offline_assimilation',

    author='Philip Brohan',
    author_email='philip.brohan@metofice.gov.uk',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],

    # Keywords for your project. What does your project relate to?
    keywords='weather observations assimilation',

    # Automatically find the software to be included
    package_dir = {'': 'modules'},
    packages=find_packages(where='modules'),


    # Other packages that your project depends on.
    install_requires=[
        'scitools-iris>=2.2',
        'cartopy>=0.16',
        'IRData>0.0',
        'Meteorographica>0.0',
        'numpy>1.13',
        'scipy>0.18',
        'pandas>0.20',
        'scikit-learn>0.19',
        'matplotlib>2.2.0',
    ],


)
