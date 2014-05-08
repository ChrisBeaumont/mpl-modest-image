#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


DESCRIPTION = "Friendlier matplotlib interaction with large images"
LONG_DESCRIPTION = open('README.md').read()
AUTHOR = 'Chris Beaumont'
AUTHOR_EMAIL = 'cbeaumont@cfa.harvard.edu'
MAINTAINER = 'Chris Beaumont'
MAINTAINER_EMAIL = 'cbeaumont@cfa.harvard.edu'
DOWNLOAD_URL = 'http://github.com/ChrisBeaumont/mpl-modest-image'
LICENSE = 'MIT'

try:
    from pypandoc import convert
    LONG_DESCRIPTION = convert(LONG_DESCRIPTION, 'rst', format='md')
except ImportError:
    pass

setup(name='ModestImage',
      version='0.1',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=['modest_image'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3']
      )
